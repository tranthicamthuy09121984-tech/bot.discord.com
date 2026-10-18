import os, math
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

@bot.tree.command(name="weather", description="Xem thời tiết chi tiết phường xã")
async def weather(interaction: discord.Interaction, thanh_pho: str, phuong: Optional[str] = None, xa: Optional[str] = None, tinh: Optional[str] = None):
    await interaction.response.defer()
    try:
        # Tạo địa chỉ: Thành phố, Phường, Xã, Tỉnh
        dia_diem_list = [thanh_pho]
        if phuong: dia_diem_list.append(phuong)
        if xa: dia_diem_list.append(xa)
        if tinh: dia_diem_list.append(tinh)
        
        # wttr.in hiểu kiểu "Ho Chi Minh, Quan 1"
        query = ",".join(dia_diem_list)
        hien_thi = ", ".join(dia_diem_list)

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://wttr.in/{query}?format=j1") as r:
                data = await r.json()
                cur = data['current_condition'][0]
                desc = cur['weatherDesc'][0]['value']
                temp = cur['temp_C']
                feel = cur['FeelsLikeC']
                
                embed = discord.Embed(title=f"Thời tiết {hien_thi}", color=0x00ff99)
                embed.add_field(name="Trạng thái", value=desc, inline=False)
                embed.add_field(name="Nhiệt độ", value=f"{temp}°C (cảm giác {feel}°C)", inline=False)
                
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Không tìm thấy {query} 😢")

# ... các lệnh khác /toan /ptb2 /chat /ping /help giữ nguyên bản cũ anh gửi ...

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))