import os, math, urllib.parse
import discord
from discord.ext import commands
import google.generativeai as genai
import aiohttp
from typing import Optional

try:
    from keep_alive import keep_alive
except:
    def keep_alive():
        pass

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

@bot.tree.command(name="chat", description="Chat voi AI")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats:
        user_chats[uid] = model.start_chat(history=[])
    resp = user_chats[uid].send_message(tin_nhan)
    await interaction.followup.send(resp.text[:2000])

@bot.tree.command(name="toan", description="Giai toan")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    await interaction.response.defer