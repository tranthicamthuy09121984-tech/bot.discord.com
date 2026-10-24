# -*- coding: utf-8 -*-
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
        return "Bot đang nghỉ ngơi 😴", 503
    return "Meo meo maoooo!! Bot Nguyez-FF UP 💥", 200

@app.route('/msn')
def msn_page():
    return "Trang MSN Nguyez"

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
    print(f"BOT {bot.user} - 阮福阮 #4850 ĐÃ ONLINE!! 💥")

@bot.tree.command(name="nghi_ngoi", description="Cho bot nghỉ ngơi")
@app_commands.describe(thoi_gian="Thời gian nghỉ (phút)")
async def nghi_ngoi(interaction: discord.Interaction, thoi_gian: float):
    global dang_nghi, task_nghi
    await interaction.response.defer()
    phut = thoi_gian
    dang_nghi = True
    await interaction.followup.send(f"....... Hoạt động sau {phut} phút nữa 😴")
    print(f"[{datetime.now()}] Tôi sẽ quay lại sau {phut} phút")
    async def cho_nghi_xong():
        global dang_nghi
        await asyncio.sleep(phut * 60)
        if dang_nghi:
            dang_nghi = False
            await interaction.channel.send(f"阮福阮 #4850 đã dậy! Sẵn sàng cân tất!! 💥")
    task_nghi = asyncio.create_task(cho_nghi_xong())

@bot.tree.command(name="bot_thuc", description="Đánh thức bot dậy")
async def bot_thuc(interaction: discord.Interaction):
    global dang_nghi, task_nghi
    if not dang_nghi:
        await interaction.response.send_message("Tôi vẫn còn ở đây, không đi đâu cả! 💥🔥")
        return
    if task_nghi:
        task_nghi.cancel()
    dang_nghi = False
    await interaction.response.send_message("Đã bỏ thời gian nghỉ ngơi, bắt đầu lại nào! 💥🔥")

GIFTCODE_LIST = {
    "meo_may_man": "**Meo iu** đã tặng bạn 100 con mèo may mắn🍀",
    "vvip_10": "**Meo iu** đã tặng bạn vvip 10, wao🍀",
    "cho_vang": "**Meo iu** đã tặng bạn 100 con chó vàng🍀"
}

@bot.tree.command(name="ptb2", description="Giải phương trình bậc 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    if a == 0:
        await interaction.response.send_message(f"x = {-c/b}" if b != 0 else "Vô nghiệm")
        return
    delta = b*b - 4*a*c
    if delta < 0:
        await interaction.response.send_message(f"Vô nghiệm delta={delta}")
    elif delta == 0:
        await interaction.response.send_message(f"Nghiệm kép x = {-b/(2*a)}")
    else:
        x1 = (-b + math.sqrt(delta))/(2*a)
        x2 = (-b - math.sqrt(delta))/(2*a)
        await interaction.response.send_message(f"x1={x1}, x2={x2}, delta={delta}")

@bot.tree.command(name="toan", description="Tính toán")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try:
        kq = eval(bieu_thuc, {"__builtins__": {}},