import os
import time
import json
import requests
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import BadRequest

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_WEBHOOK = os.getenv("TARGET_WEBHOOK")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
TEST_CHAT_ID = os.getenv("TEST_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def post_webhook(text: str):
    headers = {"Content-Type": "application/json"}
    if WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = WEBHOOK_SECRET

    payload = {"text": text}
    try:
        resp = requests.post(TARGET_WEBHOOK, json=payload, headers=headers, timeout=5)
        print("[webhook] status:", resp.status_code)
        print("[webhook] body:", resp.text)
    except Exception as e:
        print("[webhook] failed:", e)


def send_text_to_group_then_webhook(chat_id: int, text: str):
    try:
        msg = bot.send_message(chat_id, text, parse_mode="HTML")
    except BadRequest:
        # ถ้า parse_mode HTML ใช้ไม่ได้
        msg = bot.send_message(chat_id, text)

    print("[bot] sent message id:", msg.message_id)

    # POST เฉพาะ text
    post_webhook(text)


if __name__ == "__main__":
    if TEST_CHAT_ID:
        TEST_CHAT_ID = int(TEST_CHAT_ID)
        # ทดสอบส่งข้อความ
        send_text_to_group_then_webhook(TEST_CHAT_ID, "ทดสอบส่งเข้า webhook ชุดใหม่")
    else:
        print("Set TEST_CHAT_ID in .env first.")
