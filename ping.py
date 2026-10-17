import discord
from discord import app_commands

# ... (các phần khởi tạo bot, client của ông ở trên)

@bot.tree.command(name="ping", description="Kiểm tra độ trễ và tình trạng hoạt động của bot")
async def ping(interaction: discord.Interaction):
    # Tính độ trễ (latency) của bot tính bằng mili-giây (ms)
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot vẫn đang hoạt động mượt mà!\n⚡ **Độ trễ:** `{latency}ms`",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Yêu cầu bởi {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)