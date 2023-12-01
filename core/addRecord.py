import os
from dotenv import load_dotenv
import requests

# 載入環境變數
load_dotenv()

class AddRecord:

    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = os.getenv("DATABASE_ID")

    @classmethod
    def _toDatabase(cls, database_id, data):
        # 定義請求標頭
        headers = {
            "Authorization": f"Bearer {cls.NOTION_API_KEY}",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json"
        }

        # 發送 POST 請求
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data,
        )

        # 檢查回應，并返回 msg 消息
        if response.status_code == 200:
            return f"Added data successfully! 資料已成功添加到 Notion 資料庫({database_id})!"
        else:
            return f"Request failed with status code {response.status_code}, {response.text}."

    @classmethod
    def addURL(cls, contributor, title, url, content, time):
        # 包裝字典資料
        data = {
            "parent": {"database_id": cls.DATABASE_ID},
            "properties": {
                "作者": {"title": [{"text": {"content": contributor}}]},
                "標題": {"rich_text": [{"text": {"content": title}, "annotations": {"bold": True,"italic": False,"strikethrough": False,"underline": False,"code": False,"color": "yellow"}}]},
                "網址": {"url": url},
                "當時大腦内的想法": {"rich_text": [{"text": {"content": content}}]},
                "時間": {"date": {"start": time}}
            }
        }

        # 發送網路請求，返回 msg 消息
        return AddRecord._toDatabase(cls.DATABASE_ID, data)