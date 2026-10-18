import os, math
import discord
from discord.ext import commands
import google.generativeai as genai
import aiohttp

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

@bot.tree.command(name="chat", description="Chat với AI")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats:
        user_chats[uid] = model.start_chat(history=[])
    res = user_chats[uid].send_message(tin_nhan)
    await interaction.followup.send(res.text[:2000])

@bot.tree.command(name="reset", description="Xóa lịch sử")
async def reset(interaction: discord.Interaction):
    user_chats.pop(str(interaction.user.id), None)
    await interaction.response.send_message("Đã reset!", ephemeral=True)

@bot.tree.command(name="ping", description="Kiểm tra độ trễ")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="toan", description="Giải toán cùng nào!")
async def toan(interaction: discord.Interaction, phep_tinh: str):
    await interaction.response.defer()
    try:
        clean = phep_tinh.lower().replace("x", "*").replace(":", "/").replace("nhan", "*").replace("chia", "/").replace("cong", "+").replace("tru", "-")
        ket_qua = eval(clean)
        embed = discord.Embed(title="🚀 SpaceNguyez Toán Học", description=f"**{phep_tinh} = {ket_qua}**", color=0x00ff00)
        embed.set_footer(text="Thương hiệu SpaceNguyez - Tính cả chó mèo cũng hiểu!")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Chó: Gâu! Mèo: Meo! Lỗi rồi sen ơi: {e}\nGõ kiểu `2+2` hoặc `10:2` nha!")

@bot.tree.command(name="ptb2", description="Giải phương trình bậc 2")
async def ptb2(interaction: discord.Interaction, a: float, b: float, c: float):
    await interaction.response.defer()
    try:
        embed = discord.Embed(title="🚀 SpaceNguyez - Giải PT Bậc 2", description=f"**{a}x² + {b}x + {c} = 0**", color=0x00ff00)
        if a == 0:
            if b == 0:
                embed.add_field(name="Kết quả", value="Vô nghiệm / Vô số nghiệm", inline=False)
            else:
                x = -c / b
                embed.add_field(name="PT Bậc 1", value=f"x = {x}", inline=False)
        else:
            delta = b*b - 4*a*c
            embed.add_field(name="Delta", value=f"Δ = {delta}", inline=False)
            if delta < 0:
                embed.add_field(name="Kết quả", value="Vô nghiệm thực", inline=False)
            elif delta == 0:
                x = -b / (2*a)
                embed.add_field(name="Nghiệm kép", value=f"x = {x}", inline=False)
            else:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                embed.add_field(name="2 Nghiệm", value=f"x1 = {x1}\nx2 = {x2}", inline=False)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Lỗi rồi sen ơi: {e}")

@bot.tree.command(name="help", description="Xem các lệnh")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="SpaceNguyez - Danh sách lệnh", color=0x00ff00)
    embed.add_field(name="/chat [tin nhắn]", value="Chat với Gemini AI", inline=False)
    embed.add_field(name="/toan [phép tính]", value="VD: 2x3, 10:2", inline=False)
    embed.add_field(name="/ptb2 [a] [b] [c]", value="Giải ax²+bx+c=0", inline=False)
    embed.add_field(name="/weather [thành phố]", value="Xem thời tiết", inline=False)
    embed.add_field(name="/ping", value="Kiểm tra độ trễ", inline=False)
    embed.add_field(name="/reset", value="Xóa lịch sử chat", inline=False)
    embed.add_field(name="/help", value="Hiện bảng này", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="weather", description="Xem thời tiết")
async def weather(interaction: discord.Interaction, thanh_pho: str):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://wttr.in/{thanh_pho}?format=j1") as r:
                data = await r.json()
                cur = data['current_condition'][0]
                await interaction.followup.send(f"**Thời tiết {thanh_pho}:** {cur['weatherDesc'][0]['value']} - {cur['temp_C']}°C (cảm giác {cur['FeelsLikeC']}°C)")
    except:
        await interaction.followup.send(f"Không tìm thấy {thanh_pho} 😢")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))