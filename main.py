
import os
import html
import requests
from flask import Flask, request, abort

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]
BASE_URL = os.environ["RENDER_EXTERNAL_URL"].rstrip("/")

API = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def home():
    return "Ahla Akhwat Bot is running ❤️"

@app.route("/webhook/" + SECRET, methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id:
        return "OK"

    # New members
    for member in message.get("new_chat_members", []):
        name = html.escape(member.get("first_name", "عضو جديد"))
        requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"🌸❤️ أهلاً وسهلاً بـ <b>{name}</b>\nنورت جروب أحلى أخوات في الدنيا 🙂❤️",
                "parse_mode": "HTML"
            },
            timeout=15
        )

    # Member leaving
    member = message.get("left_chat_member")
    if member:
        name = html.escape(member.get("first_name", "أحد الأعضاء"))
        requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"💔 غادر الجروب <b>{name}</b>\nنتمنى له كل الخير ❤️",
                "parse_mode": "HTML"
            },
            timeout=15
        )

    return "OK"

# Connect the bot to Telegram
requests.post(
    f"{API}/setWebhook",
    json={
        "url": f"{BASE_URL}/webhook/{SECRET}",
        "secret_token": SECRET
    },
    timeout=20
).raise_for_status()
