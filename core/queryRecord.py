import os
from dotenv import load_dotenv
import requests

# 載入環境變數
load_dotenv()

class QueryRecord:

    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = os.getenv("DATABASE_ID")

    @classmethod
    def _api_query(cls, params={}):

        # 定義請求標頭
        headers = {
            "Authorization": f"Bearer {cls.NOTION_API_KEY}",
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json"
        }

        # 發送 POST 請求
        response = requests.post(
            f'https://api.notion.com/v1/databases/{cls.DATABASE_ID}/query',
            headers=headers,
            json=params
        )

        # 檢查回應，并返回 `results` 結果
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Request failed with status code {response.status_code}, {response.text}.")
            return None

    @staticmethod
    def isExistURL(url):
        # 設定參數，沒有默認查找整張表
        params = {"filter": {"property": "URL", "url": {"equals": url}}}
        result = QueryRecord._api_query(params)
        return True if len(result) != 0 else False