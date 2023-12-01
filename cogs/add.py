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
    @app_commands.describe(url="不填 `標題` 默認是 `想法`", content="現在大腦内的想法")
    async def url(self, interaction: discord.Interaction, url: Optional[str], content: str = ""):
        # 確認互動
        await interaction.response.defer()

        # 判斷消息為空，結束命令
        if not content:
            await interaction.followup.send(
                embed=EmbedTemplate.error("内容不能爲空!")
            )
            return
        
        # 是否是 URL 格式，選擇 `標題` 的文字
        if validators.url(url):
            # 啓動異步請求
            get_title_task = asyncio.create_task(Utils.getTitle(url))
        
            # 網址存在於表中，結束命令
            if QueryRecord.isExistURL(url):
                await interaction.followup.send(
                    embed=EmbedTemplate.error("URL 已存在!")
                )
                return
            
            # 等待任務完成
            await get_title_task
        
        # 準備資料
        contributor = f"@{interaction.user.name}"
        time = Utils.getTime()
        title = get_title_task.result() if validators.url(url) else "想法"

        # 執行寫入，發送實際的回應
        msg = AddRecord.addURL(contributor, title, url, content, time)
        await interaction.followup.send(
                embed=EmbedTemplate.normal(msg)
            )
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(Add(bot))