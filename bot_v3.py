import os
import discord
from discord import app_commands
from discord.ext import commands
# from dotenv import load_dotenv
# load_dotenv()
import google.generativeai as genai
from keep_alive import keep_alive

# ... (đoạn code khởi tạo bot của ông ở đây)

if __name__ == "__main__":
    keep_alive() # Giữ bot luôn thức
    bot.run("MTUzMjcyMDY1MDU0MjY0NTQyMQ.G7Affi.pbthLO1YTnj8CoLk7BvRmJLfl8e_SePsSY94y0")

# Tải cấu hình từ file .env
load_dotenv()
DISCORD_TOKEN = os.getenv("MTUzMjcyMDY1MDU0MjY0NTQyMQ.G7Affi.pbthLO1YTnj8CoLk7BvRmJLfl8e_SePsSY94y0")
GEMINI_API_KEY = os.getenv("AQ.Ab8RN6L36jbJJE6ap7i-YEGwag4thRFzq3GhT8kukGjXrT1nrQ")

# Cấu hình Gemini AI
genai.configure(api_key=AQ.Ab8RN6L36jbJJE6ap7i-YEGwag4thRFzq3GhT8kukGjXrT1nrQ)
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro", generation_config=generation_config
)

# Từ điển lưu trữ phiên chat riêng biệt cho từng người dùng (User ID -> Chat Session)
user_chats = {}

intents = discord.Intents.default()
intents.message_content = True


class ContinuousChatBot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    await self.tree.sync()
    print("\n[+] Đã đồng bộ xong hệ thống Slash Commands (/)\n")


bot = ContinuousChatBot()


@bot.event
async def on_ready():
  print("\033[92m=======================================================\033[0m")
  print("\033[92m [+] HỆ THỐNG CHAT LIÊN TỤC (NHỚ NGỮ CẢNH) ĐÃ SẴN SÀNG!\033[0m")
  print(f" [+] Bot Account: {bot.user} (ID: {bot.user.id})")
  print("\033[92m=======================================================\033[0m")


# --- LỆNH CHAT LIÊN TỤC (Dùng /chat) ---
@bot.tree.command(
    name="chat",
    description="Trò chuyện liên tục với AI (Bot sẽ nhớ các câu hỏi trước đó)",
)
@app_commands.describe(tin_nhan="Nội dung bạn muốn nhắn với AI")
async def slash_chat(interaction: discord.Interaction, tin_nhan: str):
  await interaction.response.defer(thinking=True)

  try:
    user_id = interaction.user.id

    # Nếu người này chưa chat trước đó, khởi tạo phiên chat mới
    if user_id not in user_chats:
      user_chats[user_id] = model.start_chat(history=[])

    chat_session = user_chats[1532720650542645421]

    # Gửi tin nhắn vào phiên chat (AI tự động nhớ lịch sử cũ)
    response = chat_session.send_message(tin_nhan)
    answer = response.text

    # Giới hạn ký tự của Discord (2000 ký tự)
    if len(answer) > 2000:
      answer = answer[:1997] + "..."

    await interaction.followup.send(
        f"👤 **Bạn:** {tin_nhan}\n\n🤖 **Bot:** {answer}"
    )

  except Exception as e:
    await interaction.followup.send(
        f"⚠️ Đã xảy ra lỗi trong quá trình trò chuyện: `{e}`"
    )


# --- LỆNH XÓA BỘ NHỚ (Dùng /reset để bắt đầu câu chuyện mới) ---
@bot.tree.command(
    name="reset", description="Xóa lịch sử chat cũ, bắt đầu cuộc trò chuyện mới"
)
async def slash_reset(interaction: discord.Interaction):
  user_id = interaction.user.id
  if user_id in user_chats:
    del user_chats[1532720650542645421]
  await interaction.response.send_message(
      "🧹 Đã xóa bộ nhớ cũ! Bây giờ chúng ta có thể bắt đầu câu chuyện mới hoàn toàn.",
      ephemeral=True,
  )

# --- Ping (Dùng /pong để bot xuất hiện) ---
@bot.tree.command(
    name="/ping", description="Dùng /pong để bot xuất hiện"
)
async def slash_reset(interaction: discord.Interaction):
  user_id = interaction.user.id
  if user_id in user_chats:
    del user_chats[1532720650542645421]
  await interaction.response.send_message(
      "Pong! Bot của Nguyên đây.",
      ephemeral=True,
 )

if __name__ == "__main__":
    keep_alive()  # Kích hoạt server ngầm giữ bot tỉnh thức
    bot.run("MTUzMjcyMDY1MDU0MjY0NTQyMQ.G7Affi.pbthLO1YTnj8CoLk7BvRmJLfl8e_SePsSY94y0")
# Chạy bot
bot.run('MTUzMjcyMDY1MDU0MjY0NTQyMQ.G7Affi.pbthLO1YTnj8CoLk7BvRmJLfl8e_SePsSY94y0')