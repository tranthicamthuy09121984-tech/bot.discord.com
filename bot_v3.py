import os, math, asyncio
from threading import Thread
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask

# --- GEMINI ---
try:
    from google import genai
    gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    USE_NEW_GENAI = True
except:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_client = genai
    USE_NEW_GENAI = False

# --- FLASK ---
app = Flask('')
dang_nghi = False
task_nghi = None

@app.route('/')
def home():
    global dang_nghi
    if dang_nghi:
        return "Bot dang nghi ngoi", 503
    return "Bot Nguyez-FF UP", 200

@app.route('/msn')
def msn_page():
    return "Trang MSN"

@app.route('/weather')
def weather_page():
    return "Trang Weather"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- BOT ---
intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        await self.tree.sync()

bot = Bot()
user_chats = {}

@bot.event
async def on_ready():
    print(f"BOT {bot.user} - 4850 ONLINE!!")

@bot.tree.command(name="nghi_ngoi", description="Cho bot nghi ngoi")
@app_commands.describe(thoi_gian="Thoi gian nghi (phut)")
async def nghi_ngoi(interaction: discord.Interaction, thoi_gian: float):
    global dang_nghi, task_nghi
    await interaction.response.defer()
    phut = thoi_gian
    dang_nghi = True
    await interaction.followup.send(f"Hoat dong sau {phut} phut nua")
    print(f"[{datetime.now()}] Nghi {phut} phut")
    async def cho_nghi_xong():
        global dang_nghi
        await asyncio.sleep(phut * 60)
        if dang_nghi:
            dang_nghi = False
            await interaction.channel.send(f"4850 da day!")
    task_nghi = asyncio.create_task(cho_nghi_xong())

@bot.tree.command(name="bot_thuc", description="Danh thuc bot day")
async def bot_thuc(interaction: discord.Interaction):
    global dang_nghi, task_nghi
    if not dang_nghi:
        await interaction.response.send_message("Toi van con o day!")
        return
    if task_nghi:
        task_nghi.cancel()
    dang_nghi = False
    await interaction.response.send_message("Da bo thoi gian nghi ngoi, bat dau lai nao!")

GIFTCODE_LIST = {
    "meo_may_man": "Meo iu tang 100 meo may man",
    "vvip_10": "Meo iu tang vvip 10",
    "cho_vang": "Meo iu tang 100 cho vang"
}

@bot.tree.command(name="ptb2", description="Giai pt bac 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    if a == 0:
        await interaction.response.send_message(f"x = {-c/b}" if b != 0 else "Vo nghiem")
        return
    delta = b*b - 4*a*c
    if delta < 0:
        await interaction.response.send_message(f"Vo nghiem delta={delta}")
    elif delta == 0:
        await interaction.response.send_message(f"Nghiem kep x = {-b/(2*a)}")
    else:
        x1 = (-b + math.sqrt(delta))/(2*a)
        x2 = (-b - math.sqrt(delta))/(2*a)
        await interaction.response.send_message(f"x1={x1}, x2={x2}")

@bot.tree.command(name="toan", description="Tinh toan")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try:
        kq = eval(bieu_thuc, {"__builtins__": {}}, {"math": math})
        await interaction.response.send_message(f"`{bieu_thuc}` = **{kq}**")
    except Exception as e:
        await interaction.response.send_message(f"Loi: {e}")

@bot.tree.command(name="giftcode", description="Nhap giftcode")
async def giftcode(interaction: discord.Interaction, code: str):
    code = code.lower()
    if code in GIFTCODE_LIST:
        await interaction.response.send_message(f"{GIFTCODE_LIST[code]}")
    else:
        await interaction.response.send_message("Code sai!")

@bot.tree.command(name="chat", description="Chat AI")
async def chat_cmd(interaction: discord.Interaction, tin_nhan: str):
    global dang_nghi
    if dang_nghi:
        await interaction.response.send_message("Bot dang nghi go /bot_thuc de goi day!")
        return
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats:
        user_chats[uid] = []
    user_chats[uid].append(tin_nhan)
    prompt = "\n".join(user_chats[uid][-10:])
    try:
        if USE_NEW_GENAI:
            resp = gemini_client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            text = resp.text
        else:
            model = gemini_client.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(prompt)
            text = resp.text
        await interaction.followup.send(text[:2000])
    except Exception as e:
        await interaction.followup.send(f"Loi Gemini: {e}")

@bot.tree.command(name="ping", description="Ping")
async def ping_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong {round(bot.latency*1000)}ms")

@bot.tree.command(name="reset", description="Reset chat")
async def reset_cmd(interaction: discord.Interaction):
    user_chats.pop(str(interaction.user.id), None)
    await interaction.response.send_message("Da reset!")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))