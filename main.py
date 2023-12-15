import os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 建立一個 Bot 實例
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 啟動完成時
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# 載入模組
@bot.command(help="載入一個模組")
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已載入。')

# 卸載模組
@bot.command(help="卸載一個模組")
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已卸載。')

# 重新載入模組
@bot.command(help="重新載入一個模組")
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'模組 {extension} 已重新載入。')

# 載入所有模組
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# 異步入口
async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

# 確定文件是被直接運行才執行，避免被導入的自動運行
if __name__ == "__main__":
    asyncio.run(main())