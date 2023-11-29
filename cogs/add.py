import discord
from discord.ext import commands
from discord import app_commands
import validators
from utility import Utils, EmbedTemplate
import asyncio
import aiohttp
from core.queryRecord import QueryRecord
from core.addRecord import AddRecord
from typing import Optional

# 建立一個 Cog 類別
class Add(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="url", description="添加 url 進入剪藏")
    @app_commands.describe(tags_str="添加指定標簽，不填默認為 misc")
    async def add_url(self, interaction: discord.Interaction, url: str, tags_str: Optional[str] = "misc"):
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
    
    @app_commands.command(name="list", description="添加 `清單` 事務")
    async def add_list(self, interaction: discord.Interaction, content: str, tags_str: Optional[str] = None):
        # 確認互動
        await interaction.response.defer()

        # 準備要寫入的值
        contributor = f"@{interaction.user.name}"
        tags = Utils.getTags(tags_str)
        time = Utils.getTime()

        # 取得 response 返回結果
        msg = AddRecord.addContent(contributor, content, tags, time)
        
        # 發送實際的消息回應
        await interaction.followup.send(
            embed=EmbedTemplate.normal(msg)
        )
    
    @app_commands.command(name="note", description="添加 `備忘錄` 隨記")
    async def add_note(self, interaction: discord.Interaction, content: str, tags_str: Optional[str] = None):
        # 確認互動
        await interaction.response.defer()

        # 準備要寫入的值
        contributor = f"@{interaction.user.name}"
        tags = Utils.getTags(tags_str)
        time = Utils.getTime()

        # 取得 response 返回結果
        msg = AddRecord.addContent(contributor, content, tags, time, True)
        
        # 發送實際的消息回應
        await interaction.followup.send(
            embed=EmbedTemplate.normal(msg)
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Add(bot))