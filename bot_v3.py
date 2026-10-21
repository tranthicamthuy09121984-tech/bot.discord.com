import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask
from google import genai

# --- KEEP ALIVE CHUAN CHO RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Meo meo maoooo!! Bot UP - https://bot-o-day-ubajnznma.onrender.com"

def run():
    port = int(os.environ.get("PORT", 10000)) # QUAN TRONG: Phai dung PORT cua Render
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- GEMINI ---
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
   