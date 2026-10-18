import os, math, re
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
        # FIX: Ép xóa + sync lại để hiện đủ 8 lệnh ngay
        print("Đang ép sync 8 lệnh...")
        await self.tree.sync()
        print("Sync xong! Chờ 2-3 phút + Ctrl+R là hiện đủ!")

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user} - SpaceNguyez LIVE")

# ===== 8 LỆNH =====
@bot.tree.command(name="chat", description="Chat với AI Gemini")
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

@bot.tree.command(name="toan", description="Giải toán")
async def toan(interaction: discord.Interaction, bieu_thuc: str):
    await interaction.response.defer()
    try:
        kq = eval(bieu_thuc, {"__builtins__": {}}, {"math": math, "sqrt": math.sqrt})
        await interaction.followup.send(f"**{bieu_thuc} = {kq}**")
    except Exception as e:
        await interaction.followup.send(f"Lỗi toán: {e}")

@bot.tree.command(name="ptb2", description="Giải phương trình bậc 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    await interaction.response.defer()
    delta = b*b - 4*a*c
    if delta < 0:
        await interaction.followup.send(f"Vô nghiệm! Delta = {delta}")
    elif delta == 0:
        x = -b/(2*a)
        await interaction.followup.send(f"Nghiệm kép x = {x}")
    else:
        x1 = (-b + math.sqrt(delta))/(2*a)
        x2 = (-b - math.sqrt(delta))/(2*a)
        await interaction.followup.send(f"x1 = {x1}, x2 = {x2}, Delta = {delta}")

@bot.tree.command(name="weather", description="Xem thời tiết chi tiết phường xã")
async def weather(interaction: discord.Interaction, thanh_pho: str, phuong: Optional[str] = None, xa: Optional[str] = None, tinh: Optional[str] = None):
    await interaction.response.defer()
    try:
        dia_diem_list = [thanh_pho]
        if phuong: dia_diem_list.append(phuong)
        if xa: dia_diem_list.append(xa)
        if tinh: dia_diem_list.append(tinh)
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
        await interaction.followup.send(f"Không tìm thấy {query} 😢 Lỗi: {e}")

@bot.tree.command(name="mxh", description="Tìm mạng xã hội")
async def mxh(interaction: discord.Interaction, tu_khoa: str):
    await interaction.response.defer()
    await interaction.followup.send(f"Đang tìm MXH cho: {tu_khoa} (tính năng đang phát triển)")

@bot.tree.command(name="ping", description="Check ping bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms - Chó: Gâu! Mèo: Meo!")

@bot.tree.command(name="help", description="Hướng dẫn")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="SpaceNguyez - 8 lệnh", color=0x00ff99)
    embed.description = "/chat /toan /ptb2 /weather /mxh /ping /help /reset\nChó: Gâu! Mèo: Meo! Sen 阮福阮!"
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset", description="Reset chat AI")
async def reset(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    if uid in user_chats:
        del user_chats[uid]
    await interaction.response.send_message("Đã reset! Chat mới thôi sen!")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))