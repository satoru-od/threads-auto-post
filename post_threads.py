import csv
import os
import requests
from datetime import datetime, timezone, timedelta

CSV_FILE = "posts.csv"

THREADS_USER_ID = os.environ["THREADS_USER_ID"]
THREADS_ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]

JST = timezone(timedelta(hours=9))


def now_jst():
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")


with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

target_index = None

for i, row in enumerate(rows):
    if not row.get("posted_at", "").strip():
        target_index = i
        break

if target_index is None:
    print("未投稿の行がありません。")
    raise SystemExit(0)

target = rows[target_index]
text = target["text"]

create = requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads",
    data={
        "media_type": "TEXT",
        "text": text,
        "access_token": THREADS_ACCESS_TOKEN,
    },
)

print("Create status:", create.status_code)
print("Create response:", create.text)
create.raise_for_status()

creation_id = create.json()["id"]

publish = requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish",
    data={
        "creation_id": creation_id,
        "access_token": THREADS_ACCESS_TOKEN,
    },
)

print("Publish status:", publish.status_code)
print("Publish response:", publish.text)
publish.raise_for_status()

rows[target_index]["posted_at"] = now_jst()

with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "text", "posted_at"])
    writer.writeheader()
    writer.writerows(rows)

print("投稿成功:", text)
print("posted_at:", rows[target_index]["posted_at"])
