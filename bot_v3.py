# -*- coding: utf-8 -*-
import os, discord, random, asyncio, math, psutil, time
from discord.ext import commands
from flask import Flask
from threading import Thread
from google import genai

app = Flask('')

@app.route('/')
def home():
    return "Bot của Sen đang thức! Hi Sennn"

def run():
  app.run(host='0.0.0.0',port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

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

@bot.tree.command(name="about", description="Giới thiệu về chúng tôi")
async def about(interaction: discord.Interaction):
    ram = psutil.Process().memory_info().rss / 1024 / 1024
    cpu = psutil.Process().cpu_percent(interval=0.1)
    uptime_sec = int(time.time() - start_time)
    h, m, s = uptime_sec // 3600, (uptime_sec % 3600) // 60, uptime_sec % 60
    
    sen = "<:sen:1563912637098762271>"
    python = "<:python:1563912312518213702>"

    embed = discord.Embed(
        description="阮福源 bot làm được tất cả như code, lập trình, kick, chào người mới,... Tôi được chế tạo từng mảnh bởi Phúc Nguyên★დ (phucnguyend_28882)\n\nNhà tài trợ : Meta AI & Gemini 1.5 flash. Tôi sẵn sàng làm tất cả và 24/7 bởi UptimeRobot & Render bắt đầu từ năm 2024, bạn đã sẵn sàng bước vào thế giới mới? Nếu có vui chơi ngay hôm nayy!!\n\nĐừng quên, chúng tôi còn làm thêm bot đầy đủ code như Nguyez FF (Nguyez FF™ #7665) làm Discord thành một tựa games vui nhất Việt Nam, đó chính là Free Fire một tựa games sinh tồn và sống sót phổ biến hàng đầu thế giới, Meo của sen (Meo của Sen #0591) cảm nhận đang làm chủ một con mèo, Spotify Bot (Spotify Bot#7824) cảm nhận nhạc với ứng dụng Window Media Player, Nhạc Của Tui, Zing MP3 và Youtube Music. Tiến trình thì khó đến được thành công, nhưng bạn chỉ thấy nó có vài dòng dễ,..",
        color=0x0078D4
    )
    
    embed.set_author(
        name="phucnguyend_28882",
        icon_url="https://cdn.discordapp.com/emojis/1563912637098762271.png?size=128&quality=lossless"
    )

    embed.add_field(name="Thành viên", value=f"{len(bot.users):,} tổng\n{len(bot.users):,} duy nhất", inline=True)
    embed.add_field(name="Kênh", value=f"0 tổng\n0 văn bản\n0 thoại", inline=True)
    embed.add_field(name="Tiến trình", value=f"{ram:.2f} MiB\n{cpu:.2f}% CPU", inline=True)
    embed.add_field(name="Máy chủ", value=f"{len(bot.guilds)}\n{bot.shard_count or 1} shards", inline=True)
    embed.add_field(name="Tin nhắn đã thấy", value=f"0 tin nhắn\n(-0.0/s)", inline=True)
    embed.add_field(name="Thời gian hoạt động", value=f"{h}h {m}p {s}g", inline=True)
    
    embed.set_footer(
        name="Được tạo bằng Python 💝")
        icon_url="https://cdn.discordapp.com/emojis/1563912312518213702.png?size=128&quality=lossless"

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ping", description="Test bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Xem tất cả lệnh")
async def help_cmd(interaction: discord.Interaction):
    msg = """**📜 DANH SÁCH LỆNH BOT 4850**
`/ping` - Test bot
`/about` - Xem về chúng tôi
`/weather <tỉnh>` - Xem thời tiết
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
        res = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=f"Thoi tiet hom nay o {tinh}, Viet Nam, ngan gon, co icon")
        await interaction.followup.send(f"**Thoi tiet {tinh}:**\n{res.text[:2000]}")
    except Exception as e:
        await interaction.followup.send(f"Loi weather: {e}")

@bot.tree.command(name="toan", description="Tính toán")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    try:
        kq = eval(bieu_thuc)
        await interaction.response.send_message(f"`{bieu_thuc} = {kq}`")
    except Exception as e:
        await interaction.response.send_message(f"Lỗi: {e}")

@bot.tree.command(name="ptb2", description="Giải PT bậc 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    d = b * b - 4 * a * c
    if d < 0:
        await interaction.response.send_message(f"PT {a}x²+{b}x+{c}=0 vô nghiệm Δ={d}")
    elif d == 0:
        await interaction.response.send_message(f"Nghiệm kép x={-b/(2*a)}")
    else:
        await interaction.response.send_message(f"x1={(-b+math.sqrt(d))/(2*a)}, x2={(-b-math.sqrt(d))/(2*a)}")

@bot.tree.command(name="giftcode", description="Nhận giftcode")
async def giftcode(interaction: discord.Interaction):
    code = f"4850-{random.randint(1000,9999)}-{random.randint(100,999)}"
    giftcodes.append(code)
    await interaction.response.send_message(f"🎁 Giftcode: `{code}`")

@bot.tree.command(name="reset", description="Reset")
async def reset(interaction: discord.Interaction):
    giftcodes.clear()
    await interaction.response.send_message("Đã reset🧹")

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
    except Exception as e:
        await interaction.followup.send(f"Lỗi: {e}")

@bot.tree.command(name="u", description="ú òa")
async def u(interaction: discord.Interaction):
    await interaction.response.send_message("Òaaa, bạn hú hồn chưa nè.")

@bot.tree.command(name="goiplus", description="Gói thuê bao, trải nghiệm đặc quyền")
async def goiplus(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Gói thuê bao",
        description="Gói thuê bao để trải nghiệm các đặc nhiệm bổ ích khác sau này.Mua gói sẽ được ưu tiên và trải nghiệm đặc nhiệm VVIP của Meo!",
        color=0xFFD700
    )
    await interaction.response.send_message(embed=embed)
embed.add_field(name="VVIP 1 - 100.000 / 1 năm", value="Trải nghiệm những cốt truyện mới và có lệnh cho VVIP 1.Có cảm giác sắp đến 1 cốt truyện từ những ngọn lá nhỏ...", inline=True)
embed.add_field(name="VVIP 2 - 200.000 / 1 năm", value="Thêm lệnh và ưu tiên hơn VVIP 1", inline=True)
embed.add_field(name="VVIP 3 - 300.000 / 1 năm", value="Trải nghiệm đặc nhiệm VVIP 3 nào!", inline=True)
embed.add_field(name="VVIP 4 - 400.000 / 1 năm", value="Đã tiến lên một tầm cao mới", inline=True)
embed.add_field(name="VVIP 5 - 500.000 / 1 năm", value="Đã cân bằng VVIP rồi bạn ơii", inline=True)
embed.add_field(name="VVIP 6 - 600.000 / 1 năm", value="Cố gắng thêm 4 bước nữa nào!", inline=True)
embed.add_field(name="VVIP 7 - 700.000 / 1 năm", value="Thêm nữa được không nào, bạn sẽ lên được!", inline=True)
embed.add_field(name="VVIP 8 - 800.000 / 1 năm", value="Cố lên, tôi ở đây!", inline=True)
embed.add_field(name="VVIP 9 - 900.000 / 1 năm", value="Gần max level rồi!", inline=True)
embed.add_field(name="VVIP 10 - 1.000.000 / 1 năm", value="Bá chủ Sever này..?!", inline=True)

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))