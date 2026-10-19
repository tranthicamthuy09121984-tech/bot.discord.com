import os, math, urllib.parse
import discord
from discord.ext import commands
from google import genai
import aiohttp
from flask import Flask
from threading import Thread

# --- KEEP ALIVE CHUAN CHO RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "**Meo iuu** đang online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- GEMINI MOI ---
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_chats = {}

intents = discord.Intents.default()
intents.message_content = True

class ContinuousChatBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        await self.tree.sync()
        print("Sync xong!")

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.tree.command(name="chat", description="Chat với AI")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats:
        user_chats[uid] = []
    user_chats[uid].append(tin_nhan)
    prompt = "\n".join(user_chats[uid][-10:])
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    await interaction.followup.send(resp.text[:2000])

@bot.tree.command(name="ping", description="Check ping")
async def ping(interaction: discord.Interaction):
    ms = round(bot.latency*1000)
    await interaction.response.send_message(f"Pong {ms}ms")

@bot.tree.command(name="reset", description="Reset chat")
async def reset(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    if uid in user_chats:
        del user_chats[uid]
    await interaction.response.send_message("Đã reset! 🔄")

@bot.tree.command(name="help", description="Huớng dẫn")
async def help_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("/chat /ping /reset")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))