# -*- coding: utf-8 -*-
import os, discord, random, asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread
from google import genai

app = Flask('')
@app.route('/')
def home(): return "Bot 4850 Full 9 Lenh - 0d"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run, daemon=True).start()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

giftcodes = []

@bot.event
async def on_ready():
    print(f"Bot {bot.user} da online! Full lenh!")
    await bot.tree.sync()

@bot.tree.command(name="ping", description="Test bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Xem tat ca lenh")
async def help_cmd(interaction: discord.Interaction):
    msg = """
**📜 DANH SÁCH LỆNH BOT 4850**
`/ping` - Test bot
`/weather <tỉnh>` - Xem thời tiết
`/msn <câu hỏi>` - Bói may mắn
`/toan <biểu thức>` - Tính toán
`/ptb2 <a> <b> <c>` - Giải PT bậc 2
`/giftcode` - Nhận code
`/reset` - Reset giftcode
`/bot_thuc` - Đánh thức bot
`/nghi_ngoi` - Cho bot nghỉ
`/chat <tin nhắn>` - Chat AI 0đ
"""
    await interaction.response.send_message(msg)

@bot.tree.command(name="weather", description="Xem thoi tiet")
async def weather(interaction: discord.Interaction, tinh: str):
    await interaction.response.defer()
    try:
        # Dung Gemini de tra loi thoi tiet cho 0d, khoi can API key thoi tiet
        res = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Cho thoi tiet hom nay o {tinh}, Viet Nam, ngan gon, co icon"
        )
        await interaction.followup.send(f"**Thời tiết {tinh}:**\n{res.text[:2000]}")
    except Exception as e:
        await interaction.followup.send(f"Lỗi weather: {e}")

@bot.tree.command(name="msn", description="Boi may man")
async def msn(interaction: discord.Interaction, cau_hoi: str):
    dap_an = ["Cực may mắn!", "Hơi xui nha Sen!", "50/50 thôi!", "Chắc chắn được!", "Nên nghỉ ngơi đi!", "Đại cát đại lợi!"]
    await interaction.response.send_message(f"**{cau_hoi}**\n🔮 Meo bói: **{random.choice(dap_an)}**")

@bot.tree.command(name="toan", description="Tinh toan")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try:
        kq = eval(bieu_thuc)
        await interaction.response.send_message(f"`{bieu_thuc} = {kq}`")
    except Exception as e:
        await interaction.response.send_message(f"Lỗi: {e}")

@bot.tree.command(name="ptb2", description="Giai PT bac 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    import math
    d = b*b - 4*a*c
    if d < 0: await interaction.response.send_message(f"PT {a}x²+{b}x+{c}=0 vô nghiệm Δ={d}")
    elif d == 0: await interaction.response.send_message(f"Nghiệm kép x={-b/(2*a)}")
    else: await interaction.response.send_message(f"x1={(-b+math.sqrt(d))/(2*a)}, x2={(-b-math.sqrt(d))/(2*a)}")

@bot.tree.command(name="giftcode", description="Nhan giftcode")
async def giftcode(interaction: discord.Interaction):
    code = f"4850-{random.randint(1000,9999)}-{random.randint(100,999)}"
    giftcodes.append(code)
    await interaction.response.send_message(f"🎁 Giftcode của Sen: `{code}`")

@bot.tree.command(name="reset", description="Reset giftcode")
async def reset(interaction: discord.Interaction):
    giftcodes.clear()
    await interaction.response.send_message("Đã reset hết giftcode rồi Sen!")

@bot.tree.command(name="bot_thuc", description="Danh thuc bot")
async def bot_thuc(interaction: discord.Interaction):
    await interaction.response.send_message("Dậy rồi Sen ơi! Meo tỉnh rồi đây! 😼☕")

@bot.tree.command(name="nghi_ngoi", description="Cho bot nghi")
async def nghi_ngoi(interaction: discord.Interaction):
    await interaction.response.send_message("Meo đi ngủ đây... Zzz... 😴")
    await asyncio.sleep(2)
    await interaction.followup.send("...Ngủ 5s thôi, dậy lại rồi! 😹")

@bot.tree.command(name="chat", description="Chat AI 0d")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    try:
        res = gemini_client.models.generate_content(model="gemini-3.6-flash", contents=message)
        await interaction.followup.send(res.text[:2000])
    except Exception as e:
        await interaction.followup.send(f"Lỗi: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))