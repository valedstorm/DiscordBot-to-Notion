from discord.ext import commands

from core import QueryRecord, AddRecord
from utility import EmbedTemplate

class Normal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # 機器人不處理自己的消息，避免無線循環
        if message.author == self.bot.user:
            return
        
        # 指定消息頻道
        if message.channel.name == "網址":
            # 取得正確內容
            lines = message.content.splitlines()
            try:
                name = lines[0]
                url = lines[2]
            except Exception as e:
                await message.channel.send(
                    embed=EmbedTemplate.error(lines)
                )
                print(lines)
                return

            # 檢查資料庫中有沒有重複的，耗時查詢
            if QueryRecord.isExistURL(url):
                await message.channel.send(
                    embed=EmbedTemplate.error("URL 已存在於資料庫中")
                )
                return
            
            # 寫進去資料庫
            msg = AddRecord.addURL(name, url)
            await message.channel.send(
                embed=EmbedTemplate.normal(msg)
            )

async def setup(bot):
    await bot.add_cog(Normal(bot))