import asyncio
import discord
from discord.ext import commands
from discord import app_commands

import validators

from core import QueryRecord, AddRecord
from utility import Utils, EmbedTemplate

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 測試例
    @app_commands.command(name="hello", description="Hello, world!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, world!")
    
    @app_commands.command()
    async def add(self, interaction: discord.Interaction, url: str):
        # 確認互動
        await interaction.response.defer()

        if validators.url(url):
            # 啓動異步任務（請求標題）
            get_title_task = asyncio.create_task(Utils.getTitle(url))

            # 網址存在表中，結束命令
            if QueryRecord.isExistURL(url):
                await interaction.followup.send(
                    embed=EmbedTemplate.error("URL 已存在於資料庫中")
                )
                return
            
            # 等待任務
            await get_title_task

        name = get_title_task.result()

        # 寫進資料庫
        msg = AddRecord.addURL(name, url)
        await interaction.followup.send(
            embed=EmbedTemplate.normal(msg)
        )

async def setup(bot):
    await bot.add_cog(Slash(bot))