import os
import requests
import json

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
THREADS_USER_ID = os.environ["THREADS_USER_ID"]

print("THREADS_USER_ID length:", len(THREADS_USER_ID))
print("THREADS_USER_ID head:", THREADS_USER_ID[:5])

me = requests.get(
    "https://graph.threads.net/v1.0/me",
    params={
        "fields": "id,username",
        "access_token": ACCESS_TOKEN,
    },
)

print("ME status:", me.status_code)
print(json.dumps(me.json(), ensure_ascii=False, indent=2))
me.raise_for_status()

real_id = str(me.json()["id"])
print("ME id length:", len(real_id))
print("ME id head:", real_id[:5])

if THREADS_USER_ID != real_id:
    raise SystemExit("THREADS_USER_ID is different from token's /me id. Update GitHub Secret THREADS_USER_ID.")

print("THREADS_USER_ID is correct.")
