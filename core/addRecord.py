import os
from dotenv import load_dotenv
import requests

# 載入環境變數
load_dotenv()

class AddRecord:

    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    URL_DATABASE_ID = os.getenv("URL_DATABASE_ID")
    MSG_DATABASE_ID = os.getenv("MSG_DATABASE_ID")

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
    def addURL(cls, contributor, url, title, tags, time):
        # 包裝成字典資料
        data = {
            "parent": {"database_id": cls.URL_DATABASE_ID},
            "properties": {
                "Contributor": {"title": [{"text": {"content": contributor}}]},
                "URL": {"url": url},
                "Title": {"rich_text": [{"text": {"content": title}, "annotations": {"bold": True,"italic": False,"strikethrough": False,"underline": False,"code": False,"color": "yellow"}}]},
                "Tags": {"multi_select": [{"name": tag} for tag in tags]},
                "Created_time": {"date": {"start": time}}
            }
        }

        # 發送網路請求，返回 msg 消息
        return AddRecord._toDatabase(cls.URL_DATABASE_ID, data)
    
    # List 與 Note 共用
    @classmethod
    def addContent(cls, contributor, content, tags, time, is_note = False):
        # 指定資料
        data = {
            "parent": {"database_id": cls.MSG_DATABASE_ID},
            "properties": {
                "Contributor": {"title": [{"text": {"content": contributor}}]},
                "清單": {"rich_text": [{"text": {"content": content}}]} if not is_note else {"rich_text": [{"text": {"content": ""}}]},
                "備忘錄": {"rich_text": [{"text": {"content": content}}]} if is_note else {"rich_text": [{"text": {"content": ""}}]},
                "Tags": {"multi_select": [{"name": tag} for tag in tags]},
                "Created_time": {"date": {"start": time}}
            }
        }

        # 發送請求，返回 msg 消息
        return AddRecord._toDatabase(cls.MSG_DATABASE_ID, data)