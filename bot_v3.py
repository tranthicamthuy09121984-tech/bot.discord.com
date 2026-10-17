import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai

# import keep_alive, nếu không có file này trên Render thì xóa dòng này đi
try:
    from keep_alive import keep_alive
except:
    def keep_alive():
        pass

# --- 1. Cấu hình AI ---
GOOGLE_API_KEY = os.getenv("AQ.Ab8RN6Lk46aQcy_LKeg9VbwD0x13E4bQ0zbKHv15FTbZBQgkTw")
DISCORD_TOKEN = os.getenv("MTUzMjcyMDY1MDU0MjY0NTQyMQ.GWYd9y.D-O_43NdKsOozcGoh1Vvnd9OLyAPcTqUaPBgBI")

genai.configure(api_key=AQ.Ab8RN6Lk46aQcy_LKeg9VbwD0x13E4bQ0zbKHv15FTbZBQgkTw)
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config={"temperature": 0.7}
)

user_chats = {} # Lưu lịch sử chat riêng cho từng người

# --- 2. Khởi tạo Bot ---
intents = discord.Intents.default()
intents.message_content = True

class ContinuousChatBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Đã đồng bộ Slash Commands!")

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot của Nguyên đã online! {bot.user}")

# --- 3. Lệnh Slash ---
@bot.tree.command(name="chat", description="Chat với AI Gemini")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    
    if user_id not in user_chats:
        user_chats[1532720650542645421] = model.start_chat(history=[])
    
    try:
        response = user_chats[1532720650542645421].send_message(tin_nhan)
        text = response.text
        # Cắt ngắn nếu quá 2000 ký tự
        if len(text) > 2000:
            text = text[:1997] + "..."
        await interaction.followup.send(text)
    except Exception as e:
        await interaction.followup.send(f"Lỗi: {e}")

@bot.tree.command(name="reset", description="Xóa lịch sử chat")
async def reset(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_chats:
        del user_chats[1532720650542645421]
    await interaction.response.send_message("Đã xóa lịch sử chat, bắt đầu lại nhé!", ephemeral=True)

@bot.tree.command(name="ping", description="Kiểm tra bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Bot của Nguyên đây. Ping: {round(bot.latency*1000)}ms")

# --- 4. Chạy 24/7 ---
keep_alive()
bot.run(MTUzMjcyMDY1MDU0MjY0NTQyMQ.GWYd9y.D-O_43NdKsOozcGoh1Vvnd9OLyAPcTqUaPBgBI)