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

def bo_dau(s):
    s = s.lower()
    rep = {
        'á':'a','à':'a','ả':'a','ã':'a','ạ':'a',
        'ă':'a','ắ':'a','ằ':'a','ẳ':'a','ẵ':'a','ặ':'a',
        'â':'a','ấ':'a','ầ':'a','ẩ':'a','ẫ':'a','ậ':'a',
        'é':'e','è':'e','ẻ':'e','ẽ':'e','ẹ':'e',
        'ê':'e','ế':'e','ề':'e','ể':'e','ễ':'e','ệ':'e',
        'í':'i','ì':'i','ỉ':'i','ĩ':'i','ị':'i',
        'ó':'o','ò':'o','ỏ':'o','õ':'o','ọ':'o',
        'ô':'o','ố':'o','ồ':'o','ổ':'o','ỗ':'o','ộ':'o',
        'ơ':'o','ớ':'o','ờ':'o','ở':'o','ỡ':'o','ợ':'o',
        'ú':'u','ù':'u','ủ':'u','ũ':'u','ụ':'u',
        'ư':'u','ứ':'u','ừ':'u','ử':'u','ữ':'u','ự':'u',
        'ý':'y','ỳ':'y','ỷ':'y','ỹ':'y','ỵ':'y',
        'đ':'d'
    }
    return "".join(rep.get(c, c) for c in s)

class ContinuousChatBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        print("Đang ép sync 8 lệnh...")
        await self.tree.sync()
        print("Sync xong!")

bot = ContinuousChatBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

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
        expr = bieu_thuc.replace("^", "**").replace("x", "*").strip()
        kq = eval(expr, {"__builtins__": {}}, {"math": math, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos})
        await interaction.followup.send(f"**{bieu_thuc} = {kq}**")
    except Exception as e:
        try:
            uid = str(interaction.user.id)
            if uid not in user_chats:
                user_chats[uid] = model.start_chat(history=[])
            resp = user_chats[uid].send_message(f"Giải toán: {bieu_thuc}, chỉ trả lời kết quả ngắn gọn")
            await interaction.followup.send(f"**{bieu_thuc} = {resp.text[:500]}** (AI giải)")
        except:
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
    query_goc = ", ".join([x for x in [thanh_pho, phuong, xa, tinh] if x])
    try:
        query_khong_dau = bo_dau(query_goc)
        query = urllib.parse.quote(query_khong_dau)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://wttr.in/{query}?format=j1") as r:
                text = await r.text()
                if "Unknown location" in text:
                    raise Exception("Unknown location")
                data = await r.json(content_type=None)
                cur = data['current_condition'][0]
                embed = discord.Embed(title=f"Thời tiết {query_goc}", color=0x00ff99)
                embed.add_field(name="Trạng thái", value=cur['weatherDesc'][0]['value'], inline=False)
                embed.add_field(name="Nhiệt độ", value=f"{cur['temp_C']}°C (cảm giác {cur['FeelsLikeC']}°C)", inline=False)
                embed.add_field(name="Độ ẩm", value=f"{cur['humidity']}%", inline=False)
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Không tìm thấy {query_goc} 😢 Thử: Ho Chi Minh | Lỗi: {e}")

@bot.tree.command(name="mxh", description="Tìm mạng xã hội")
async def mxh(interaction: discord.Interaction, tu_khoa: str):
    await interaction.response.defer()
    await interaction.followup.send(f"Đang tìm MXH cho: {tu_khoa}")

@bot.tree.command(name="ping", description="Check ping bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Hướng dẫn")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="SpaceNguyez - 8 lệnh", color=0x00ff99)
    embed.description = "/chat /toan /ptb2 /weather /mxh /ping /help /reset"
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset", description="Reset chat AI")
async def reset(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    if uid in user_chats:
        del user_chats[uid]
    await interaction.response.send_message("Đã reset!")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))