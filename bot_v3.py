import os, math, re, urllib.parse
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
        print("Đang ép sync lệnh...")
        await self.tree.sync()
        print("Sync xong!")

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.tree.command(name="chat", description="💬 Chat với AI Gemini")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    try:
        uid = str(interaction.user.id)
        if uid not in user_chats:
            user_chats[uid] = model.start_chat(history=[])
        resp = user_chats[uid].send_message(tin_nhan)
        await interaction.followup.send(resp.text[:2000])
    except Exception as e:
        await interaction.followup.send(f"Lỗi: {e}")

@bot.tree.command(name="toan", description="🔢 Giải toán")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    await interaction.response.defer()
    try:
        expr = bieu_thuc.replace("^", "**").replace("x", "*").strip()
        kq =