import discord
from discord.ext import commands
import asyncio

# ==== DÁN TOKEN MỚI VÀO ĐÂY ====
# Token mới của Nguyên
TOKEN = "MTUzMjcyMDY1MDU0MjY0NTQyMQ.GARqxu.98xmBfsY2M89ahXC0_icih3IB5603_rjww8lso"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("=================================")
    print(f"  BOT DA ONLINE: {bot.user}")
    print("=================================")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

# Chạy bot, tự bắt lỗi
try:
    TOKEN = "AQ.Ab8RN6L36jbJJE6ap7i-YEGwag4thRFzq3GhT8kukGjXrT1nrQ"
except discord.errors.LoginFailure:
    print("LOI: Token sai!")
except Exception as e:
    print(f"Loi khac: {e}")

input("An Enter de thoat...")