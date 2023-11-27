import discord
from discord.ext import commands
from discord import app_commands

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # name 指令表示呼叫的名稱，不能使用大寫英文，description 顯示描述
    @app_commands.command(name = "hello", description = "Hello, world!")
    async def hello(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        await interaction.response.send_message("Hello, world!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))