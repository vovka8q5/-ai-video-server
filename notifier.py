# notifier.py

import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram token или chat_id не задан!")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ Ошибка при отправке Telegram: {response.text}")
        else:
            print("✅ Уведомление Telegram отправлено")
    except Exception as e:
        print(f"❌ Telegram ошибка: {e}")
