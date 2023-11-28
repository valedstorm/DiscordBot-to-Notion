import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 事件：機器人已啟動
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'目前登入身份 --> {bot.user}')
    print(f"載入 {len(slash)} 個斜線指令")

# 指令：載入模組
@bot.command(help="載入一個模組")
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已載入。')

# 指令：卸載模組
@bot.command(help="卸載一個模組")
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已卸載。')

# 指令：重新載入模組
@bot.command(help="重新載入一個模組")
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已重新載入。')

# 函數：載入所有模組
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# 異步函數：主入口
async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

# 確保文件被直接運行時才執行 bot.run() 函數，避免導入時自動運行
if __name__ == "__main__":
    asyncio.run(main())