import discord
from datetime import datetime
import pytz
import asyncio
import aiohttp
import validators
from bs4 import BeautifulSoup

class Utils:
    # 取得標簽：以空白切割字符串，並去除每一個元素的前後空白，轉小寫
    @staticmethod
    def getTags(input_string):
        processed_list = [tag.strip().lower() for tag in input_string.split()]
        unique_list = list(set(processed_list))
        return unique_list
    
    # 時區時間
    @staticmethod
    def getTime():
        # 取得系統時區
        timezone = datetime.now(pytz.timezone('UTC')).astimezone().tzinfo
        # 取得時間
        time = datetime.now(timezone).isoformat()
        return time
    
    # 異步網路請求
    @staticmethod
    async def getTitle(url):
        async with aiohttp.ClientSession() as session:
            # 模擬正常請求頭
            headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" }
            # 發送 GET 請求
            async with session.get(url, headers=headers) as response:
                # 檢查請求是否成功
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "No title found"
                    return title
                else:
                    print(f"Failed to fetch {url}. Status code: {response.status}")
                    return None
