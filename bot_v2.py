import os
import time
import discord
from google import genai
from dotenv import load_dotenv

# Tải biến cấu hình bảo mật
load_dotenv()

# Cấu hình quyền hạn nâng cao cho Discord Bot (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Khởi tạo client bot
client = discord.Client(intents=intents)

# Khởi tạo Google GenAI client
ai_client = genai.Client(api_key="AQ.Ab8RN6KuplibIteCyyMkFRLy53CpFIbZnwCAeukN5IrzPvxujw")

@client.event
async def on_ready():
    print("\033[92m" + "="*55 + "\033[0m")
    print("\033[92m" + f" [+] HỆ THỐNG ĐÃ NÂNG CẤP THÀNH CÔNG!" + "\033[0m")
    print(f" [+] Bot Account: {client.user} (ID: {client.user.id})")
    print(" [+] Trạng thái: Sẵn sàng xử lý lệnh qua tiền tố '!hoi'")
    print("\033[92m" + "="*55 + "\033[0m")

@client.event
async def on_message(message):
    # Bỏ qua tin nhắn của chính bot để tránh lặp vô hạn
    if message.author == client.user:
        return

    # Xử lý lệnh nâng cấp !hoi
    if message.content.startswith('!hoi '):
        user_message = message.content[5:].strip()
        
        if not user_message:
            await message.channel.send("⚠️ Ông trùm chưa nhập nội dung câu hỏi sau lệnh `!hoi` kìa!")
            return

        # Gửi thông báo đang xử lý (tạo cảm giác chuyên nghiệp)
        typing_msg = await message.channel.send("🔄 Đang kết nối mô hình Gemini để phân tích dữ liệu...")

        try:
            # Gửi yêu cầu phân tích nội dung đến Google GenAI
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
            
            # Xóa tin nhắn chờ và trả về kết quả chuẩn xác
            await typing_msg.delete()
            await message.channel.send(response.text)
            
        except Exception as e:
            await typing_msg.delete()
            await message.channel.send(f"❌ [LỖI HỆ THỐNG]: Không thể xử lý yêu cầu. Chi tiết: `{str(e)}`")

# Kích hoạt vận hành bot
client.run("MTUzMjcyMDY1MDU0MjY0NTQyMQ.GzfXcB.BgAs_vCOuXoxLdWJd8lhUiopqPEEnLU39lFjBo")