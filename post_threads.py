import os
import requests

ACCESS_TOKEN = os.environ["INSTAGRAM_ACCESS_TOKEN"]
IG_USER_ID = os.environ["INSTAGRAM_BUSINESS_ID"]

TEXT = "GitHub Actionsから初めてThreadsへ自動投稿しました！"

# 投稿コンテナ作成
url = f"https://graph.threads.net/v1.0/{IG_USER_ID}/threads"

r = requests.post(
    url,
    data={
        "media_type": "TEXT",
        "text": TEXT,
        "access_token": ACCESS_TOKEN,
    },
)

print(r.status_code)
print(r.text)
r.raise_for_status()

creation_id = r.json()["id"]

# 公開
publish_url = f"https://graph.threads.net/v1.0/{IG_USER_ID}/threads_publish"

r = requests.post(
    publish_url,
    data={
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    },
)

print(r.status_code)
print(r.text)
r.raise_for_status()

print("投稿成功")
