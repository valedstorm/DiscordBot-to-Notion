import discord
from discord.ext import commands
from discord import app_commands
import validators
from utility import Utils, EmbedTemplate
import asyncio
import aiohttp
from core.queryRecord import QueryRecord
from core.addRecord import AddRecord

# 建立一個 Cog 類別
class Add(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "url", description = "添加 url 進入剪藏")
    async def add_url(self, interaction: discord.Interaction, url: str, tags_str: str):
        # 確認互動
        await interaction.response.defer()
        
        # 檢查 url 格式
        if validators.url(url):
            # 啓動異步任務
            get_title_task = asyncio.create_task(Utils.getTitle(url))
            
            if not QueryRecord.isExistURL(url):
                # 準備要寫入的值
                contributor = f"@{interaction.user.name}"
                tags = Utils.getTags(tags_str)
                time = Utils.getTime()
                await get_title_task
                title = get_title_task.result()
                
                # 執行寫入，返回消息
                msg = AddRecord.addURL(contributor, url, title, tags, time)
                # 發送實際的回應
                await interaction.followup.send(
                    embed=EmbedTemplate.normal(msg)
                )
                return
            else:
                await interaction.followup.send(
                    # embed=EmbedTemplate.normal(msg, title="使用示例"), ephemeral=True
                    embed=EmbedTemplate.error("URL 已存在")
                )
                return
        else:
            await interaction.followup.send(
                embed=EmbedTemplate.error("無效的 URL 格式")
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Add(bot))