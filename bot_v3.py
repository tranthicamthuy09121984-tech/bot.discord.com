import os, random, math
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
from google import genai

app = Flask('')
@app.route('/')
def home():
    return "Meo meo maoooo!! Bot Nguyez-FF UP"
@app.route('/msn')
def msn_page():
    return "Trang MSN Nguyez"
@app.route('/weather')
def weather_page():
    return "Trang Weather"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_chats = {}
intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        await self.tree.sync()

bot = Bot()
@bot.event
async def on_ready():
    print(f"Bot {bot.user} online")

GIFTCODE_LIST = {
    "meo_may_man": "**Meo iu** đã tặng bạn 100 mèo mèo may mắn🍀",
    "vvip_10": "**Meo iu** đã tặng bạn vvip 10, wao🍀",
    "cho_vang": "**Meo iu** đã tặng bạn 100 con chó vàng🍀"
}

@bot.tree.command(name="ptb2", description="Giai pt bac 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    if a == 0:
        await interaction.response.send_message(f"x = {-c/b}" if b!=0 else "Vo nghiem")
        return
    delta = b*b - 4*a*c
    if delta < 0:
        await interaction.response.send_message(f"Vo nghiem delta={delta}")
    elif delta == 0:
        await interaction.response.send_message(f"Nghiem kep x = {-b/(2*a)}")
    else:
        x1 = (-b + math.sqrt(delta))/(2*a)
        x2 = (-b - math.sqrt(delta))/(2*a)
        await interaction.response.send_message(f"x1={x1}, x2={x2}, delta={delta}")

@bot.tree.command(name="toan", description="Tinh toan")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try:
        kq = eval(bieu_thuc, {"__builtins__": {}}, {"math": math, "sqrt": math.sqrt})
        await interaction.response.send_message(f"`{bieu_thuc}` = **{kq}**")
    except Exception as e:
        await interaction.response.send_message(f"Loi: {e}")

@bot.tree.command(name="giftcode", description="Nhap giftcode")
async def giftcode(interaction: discord.Interaction, code: str):
    code = code.lower()
    if code in GIFTCODE_LIST:
        await interaction.response.send_message(f"🎁 {GIFTCODE_LIST[code]}")
    else:
        await interaction.response.send_message("❌ Code sai! Code: `meo_may_man`, `vvip_10`, `cho_vang`")

@bot.tree.command(name="msn", description="MSN")
async def msn_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("📦 Trang MSN: https://nguyez-ff.onrender.com/msn")

@bot.tree.command(name="mxh", description="MXH")
async def mxh_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("🌐 @nguyez.ff")

@bot.tree.command(name="weather", description="Thoi tiet")
async def weather_cmd(interaction: discord.Interaction, thanh_pho: str):
    await interaction.response.send_message(f"🌤️ {thanh_pho}")

@bot.tree.command(name="help", description="Help")
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("/ptb2 /toan /giftcode /msn /mxh /weather /chat /ping /reset")

@bot.tree.command(name="chat", description="Chat AI")
async def chat_cmd(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats: user_chats[uid] = []
    user_chats[uid].append(tin_nhan)
    prompt = "\n".join(user_chats[uid][-10:])
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    await interaction.followup.send(resp.text[:2000])

@bot.tree.command(name="ping", description="Ping")
async def ping_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong {round(bot.latency*1000)}ms")

@bot.tree.command(name="reset", description="Reset")
async def reset_cmd(interaction: discord.Interaction):
    user_chats.pop(str(interaction.user.id), None)
    await interaction.response.send_message("Da reset!")

@bot.tree.command(name="ban", description="Ban")
async def ban_cmd(interaction: discord.Interaction, ten: str):
    await interaction.response.send_message(f"Ban {ten}")

@bot.tree.command(name="quay", description="Quay")
async def quay_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Trung MP40 Mang Xa!")

@bot.tree.command(name="chon_che_do", description="Chon che do")
async def chon_che_do_cmd(interaction: discord.Interaction, che_do: str):
    await interaction.response.send_message(f"Da chon {che_do}")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))