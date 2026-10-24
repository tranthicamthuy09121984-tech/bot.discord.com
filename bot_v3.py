# -*- coding: utf-8 -*-
import os, discord, random, asyncio, math, psutil, time
from discord.ext import commands
from flask import Flask
from threading import Thread
from google import genai

app = Flask('')
@app.route('/')
def home(): return "Bot 4850 Full 9 Lenh - Online"
def run_flask(): app.run(host='0.0.0.0', port=8080)
Thread(target=run_flask, daemon=True).start()

start_time = time.time()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
giftcodes = []

@bot.event
async def on_ready():
    print(f"Bot {bot.user} da online!")
    await bot.tree.sync()

@bot.tree.command(name="stats", description="Xem stats giong Carl-bot")
async def stats(interaction: discord.Interaction):
    embed = discord.Embed(title="Nguyễn Phúc Nguyên bot", color=0x0078D4)
    embed.add_field(name="Servers", value=str(len(bot.guilds)))
    embed.add_field(name="Members", value=str(len(bot.users)))
    embed.add_field(name="RAM", value=f"{psutil.Process().memory_info().rss/1024/1024:.2f} MiB")
    embed.add_field(name="Uptime", value=f"{(time.time()-start_time)/3600:.1f}h")
    try:
        file = discord.File("python_trang_xanh.png", filename="python.png")
        embed.set_thumbnail(url="attachment://python.png")
        await interaction.response.send_message(embed=embed, file=file)
    except:
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Test bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Xem tat ca lenh")
async def help_cmd(interaction: discord.Interaction):
    msg = """**📜 DANH SÁCH LỆNH BOT 4850**
`/ping` - Test bot
`/stats` - Xem stats
`/weather <tỉnh>` - Xem thời tiết
`/msn` - Mở MSN
`/toan <biểu thức>` - Tính toán
`/ptb2 <a> <b> <c>` - Giải PT bậc 2
`/giftcode` - Nhận code
`/reset` - Reset giftcode
`/bot_thuc` - Đánh thức bot
`/nghi_ngoi` - Cho bot nghỉ
`/chat <tin nhắn>` - Chat AI 0đ"""
    await interaction.response.send_message(msg)

@bot.tree.command(name="weather", description="Xem thoi tiet")
async def weather(interaction: discord.Interaction, tinh: str):
    await interaction.response.defer()
    try:
        res = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=f"Chờ thời tiết hôm nay ở {tinh}, Viet Nam, ngắn gọn, có icon")
        await interaction.followup.send(f"**Thời tiết {tinh}:**\n{res.text[:2000]}")
    except Exception as e: await interaction.followup.send(f"Lỗi weather: {e}")

@bot.tree.command(name="toan", description="Tính toán")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try: kq = eval(bieu_thuc); await interaction.response.send_message(f"`{bieu_thuc} = {kq}`")
    except Exception as e: await interaction.response.send_message(f"Lỗi: {e}")

@bot.tree.command(name="ptb2", description="Giải PT bậc 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    d = b*b - 4*a*c
    if d < 0: await interaction.response.send_message(f"PT {a}x²+{b}x+{c}=0 vô nghiệm Δ={d}")
    elif d == 0: await interaction.response.send_message(f"Nghiệm kép x={-b/(2*a)}")
    else: await interaction.response.send_message(f"x1={(-b+math.sqrt(d))/(2*a)}, x2={(-b-math.sqrt(d))/(2*a)}")

@bot.tree.command(name="giftcode", description="Nhận giftcode")
async def giftcode(interaction: discord.Interaction):
    code = f"4850-{random.randint(1000,9999)}-{random.randint(100,999)}"
    giftcodes.append(code)
    await interaction.response.send_message(f"🎁 Giftcode: `{code}`")

@bot.tree.command(name="reset", description="Reset giftcode")
async def reset(interaction: discord.Interaction):
    giftcodes.clear(); await interaction.response.send_message("Đã reset hết giftcode!")

@bot.tree.command(name="bot_thuc", description="Danh thuc bot")
async def bot_thuc(interaction: discord.Interaction):
    await interaction.response.send_message("Dậy rồi Sen ơi! Meo tỉnh rồi đây! 😼☕")

@bot.tree.command(name="nghi_ngoi", description="Cho bot nghi")
async def nghi_ngoi(interaction: discord.Interaction):
    await interaction.response.send_message("Meo đi ngủ đây... Zzz... 😴")
    await asyncio.sleep(2)
    await interaction.followup.send("...Ngủ 5s thôi, dậy lại rồi! 😹")

@bot.tree.command(name="chat", description="Chat AI")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    try:
        res = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=message)
        await interaction.followup.send(res.text[:2000])
    except Exception as e: await interaction.followup.send(f"Lỗi: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))