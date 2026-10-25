# -*- coding: utf-8 -*-
import os, discord, random, asyncio, math, psutil, time
from discord.ext import commands
from flask import Flask
from threading import Thread
from google import genai

app = Flask('')
@app.route('/')
def home():
    return "阮福源 bot Full 9 Lệnh - Online"

def run_flask():
    # QUAN TRỌNG: Dùng PORT của Render, không fix 8080
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_flask, daemon=True).start()
# bot.run(os.getenv("DISCORD_TOKEN"))

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

@bot.tree.command(name="about", description="Giới thiệu về chúng tôi")
async def about(interaction: discord.Interaction):
    ram = psutil.Process().memory_info().rss / 1024 / 1024
    cpu = psutil.Process().cpu_percent(interval=0.1)
    uptime_sec = int(time.time() - start_time)
    h, m, s = uptime_sec//3600, (uptime_sec%3600)//60, uptime_sec%60

sen = ":sen:"
    embed.set_author(name=f"{sen} Người tạo")
        embed = discord.Embed(
        title="阮福源 bot",
        description="阮福源 bot làm được tất cả như code, lập trình, kick, chào người mới,... Tôi được chế tạo từng mảnh bởi Phúc Nguyên★დ (phucnguyend_28882) Nhà tài trợ : Meta AI & Gemini 1.5 flash. Tôi sẫn sàng làm tất cả và 24/7 bởi UptimeRobot & Render bắt đầu từ năm 2024, bạn đã sẫn sàng bước vào thế giới mới? Nếu có vui chơi ngay hôm nayy!! Đừng quên, chúng tôi còn làm thêm bot đầy đủ code như Nguyez FF (Nguyez FF™ #7665) làm Discord thành một tựa games vui nhất Việt Nam, đó chính là Free Fire một tựa games sinh tồn và sống sót phổ biến hàng đầu thế giới, Meo của sen (Meo của Sen #0591) cảm nhận đang làm chủ một con mèo, Spotify Bot (Spotify Bot#7824) cảm nhận nhạc với ứng dụng Windown Media Player, Nhạc Của Tui, Zing MP3 và Youtube Music. Tiến trình thì khó đến được thành công, nhưng bạn chỉ thấy nó có vài dòng dễ,..",
        color=0x0078D4
    )

    embed.add_field(name="Thành viên", value=f"{len(bot.users):,} tổng\n{len(bot.users):,} duy nhất", inline=True)
    embed.add_field(name="Kênh", value=f"0 tổng\n0 văn bản\n0 thoại", inline=True)
    embed.add_field(name="Tiến trình", value=f"{ram:.2f} MiB\n{cpu:.2f}% CPU", inline=True)

    embed.add_field(name="Máy chủ", value=f"{len(bot.guilds)}\n{bot.shard_count or 1} shards", inline=True)
    embed.add_field(name="Tin nhắn đã thấy", value=f"0 tin nhắn\n(-0.0/s)", inline=True)
    embed.add_field(name="Thời gian hoạt động", value=f"{h}h {m}p {s}g", inline=True)
emoji = ":python:"
embed.set_footer(text=f"{emoji} Được tạo bằng Pythonn 💝")

@bot.tree.command(name="ping", description="Test bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Xem tất cả lệnh")
async def help_cmd(interaction: discord.Interaction):
    msg = """**📜 DANH SÁCH LỆNH BOT 4850**
`/ping` - Test bot
`/about` - Xem về chúng tôi
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

@bot.tree.command(name="reset", description="Reset")
async def reset(interaction: discord.Interaction):
    giftcodes.clear(); await interaction.response.send_message("Đã reset🧹")

@bot.tree.command(name="bot_thuc", description="Đánh thức bot")
async def bot_thuc(interaction: discord.Interaction):
    await interaction.response.send_message("Dậy rồi bạn ơi! Mình tỉnh rồi đây! 😼☕")

@bot.tree.command(name="nghi_ngoi", description="Cho bot nghỉ")
async def nghi_ngoi(interaction: discord.Interaction):
    await interaction.response.send_message("Mình đi ngủ đây... Zzz... 😴")
    await asyncio.sleep(2)
    await interaction.followup.send("...Ngủ 5s thôi, dậy lại rồi! 😹")

@bot.tree.command(name="chat", description="Chat AI")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    try:
        res = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=message)
        await interaction.followup.send(res.text[:2000])
    except Exception as e: await interaction.followup.send(f"Lỗi: {e}")

@bot.tree.command(name="u", description="ú òa")
async def u(interaction: discord.Interaction):
    await interaction.response.send_message("Òaaa, bạn hú hồn chưa nè.")
bot.run(os.getenv("DISCORD_TOKEN"))