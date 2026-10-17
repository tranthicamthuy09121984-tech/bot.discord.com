import os
import discord
from discord.ext import commands
import google.generativeai as genai

# Fix keep_alive nếu thiếu
try:
    from keep_alive import keep_alive
except:
    def keep_alive():
        pass

# Lấy key từ Render Environment - ĐỪNG DÁN THẲNG KEY VÔ ĐÂY
genai.configure(api_key=os.getenv("AQ.Ab8RN6Lk46aQcy_LKeg9VbwD0x13E4bQ0zbKHv15FTbZBQgkTw"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.7}
)

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

@bot.tree.command(name="chat", description="Chat với AI")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats:
        user_chats[uid] = model.start_chat(history=[])
    res = user_chats[uid].send_message(tin_nhan)
    text = res.text[:2000]
    await interaction.followup.send(text)

@bot.tree.command(name="reset", description="Xóa chat")
async def reset(interaction: discord.Interaction):
    user_chats.pop(str(interaction.user.id), None)
    await interaction.response.send_message("Đã reset!", ephemeral=True)

@bot.tree.command(name="ping", description="Ping bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

keep_alive()
bot.run(os.getenv("MTUzMjcyMDY1MDU0MjY0NTQyMQ.GWYd9y.D-O_43NdKsOozcGoh1Vvnd9OLyAPcTqUaPBgBI"))