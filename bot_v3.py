import os, discord
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
    def __init__(self): super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self): await self.tree.sync()
bot = ContinuousChatBot()

@bot.event
async def on_ready(): print(f"Bot online: {bot.user}")

@bot.tree.command(name="chat", description="Chat với AI")
async def chat(interaction: discord.Interaction, tin_nhan: str):
    await interaction.response.defer()
    uid = str(interaction.user.id)
    if uid not in user_chats: user_chats[uid] = model.start_chat(history=[])
    res = user_chats[uid].send_message(tin_nhan)
    await interaction.followup.send(res.text[:2000])

@bot.tree.command(name="reset", description="Xóa lịch sử")
async def reset(interaction: discord.Interaction):
    user_chats.pop(str(interaction.user.id), None)
    await interaction.response.send_message("Da reset!", ephemeral=True)

@bot.tree.command(name="ping", description="Kiem tra bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="help", description="Xem các lệnh")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="URobot - Danh sách lệnh", color=0x00ff00)
    embed.add_field(name="/chat [tin nhắn]", value="Chat với Gemini AI", inline=False)
    embed.add_field(name="/weather [thành phố]", value="Xem thời tiết. VD: Ho Chi Minh", inline=False)
    embed.add_field(name="/ping", value="Kiem tra do tre", inline=False)
    embed.add_field(name="/reset", value="Xoa lich su chat", inline=False)
    embed.add_field(name="/help", value="Hien bang nay", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="weather", description="Xem thời tiết")
async def weather(interaction: discord.Interaction, thanh_pho: str):
    await interaction.response.defer()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://wttr.in/{thanh_pho}?format=j1") as r:
                data = await r.json()
                cur = data['current_condition'][0]
                await interaction.followup.send(f"**Thoi tiet {thanh_pho}:** {cur['weatherDesc'][0]['value']} - {cur['temp_C']}°C (cam giac {cur['FeelsLikeC']}°C)")
    except:
        await interaction.followup.send(f"Khong tim thay {thanh_pho} 😢")

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))