import os, math, urllib.parse
import discord
from discord.ext import commands
import google.generativeai as genai
import aiohttp
from typing import Optional

try:
    from keep_alive import keep_alive
except:
    def keep_alive(): pass

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.5-flash")
user_chats = {}

intents = discord.Intents.default()
intents.message_content = True

class ContinuousChatBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        await self.tree.sync()

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.tree.command(name="chat", description="Chat voi AI Gemini")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    try:
        uid = str(interaction.user.id)
        if uid not in user_chats:
            user_chats[uid] = model.start_chat(history=[])
        resp = user_chats[uid].send_message(tin_nhan)
        await interaction.followup.send(resp.text[:2000])
    except Exception as e:
        await interaction.followup.send(f"Loi: {e}")

@bot.tree.command(name="toan", description="Giai toan")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    await interaction.response.defer()
    try:
        expr = bieu_thuc.replace("^", "**").replace("x", "*").replace("X", "*").strip()
        if not expr:
            await interaction.followup.send("Nhap bieu thuc VD: 2+2")
            return
        kq = eval(expr, {"__builtins__": {}}, {"math": math, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos})
        await interaction.followup.send(f"{bieu_thuc} = {kq}")
    except Exception:
        try:
            uid = str(interaction.user.id)
            if uid not in user_chats:
                user_chats[uid] = model.start_chat(history=[])
            resp = user_chats[uid].send_message(f"Giai toan {bieu_thuc}, tra loi ngan gon")
            await interaction.followup.send(f"{bieu_thuc} = {resp.text[:500]} (AI giai)")
        except:
            await interaction.followup.send("Bieu thuc sai cu phap")

@bot.tree.command(name="ptb2", description="Giai PT bac 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    await interaction.response.defer()
    delta = b*b - 4*a*c
    if delta < 0:
       