# listener_user.py
import os
import asyncio
import json
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import ClientSession

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")   # preferred for user session
BOT_TOKEN = os.getenv("BOT_TOKEN")             # optional fallback
TARGET_WEBHOOK = os.getenv("TARGET_WEBHOOK")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
WATCH_CHATS = os.getenv("WATCH_CHATS") or ""    # comma separated chat ids or usernames, empty = all

if not TARGET_WEBHOOK:
    print("Missing TARGET_WEBHOOK in env")
    raise SystemExit(1)
if not API_ID or not API_HASH:
    print("Missing API_ID / API_HASH in env")
    raise SystemExit(1)

API_ID = int(API_ID)

# build client
if STRING_SESSION:
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    print("Using user StringSession")
elif BOT_TOKEN:
    client = TelegramClient("bot-session", API_ID, API_HASH)
    print("Using bot token (fallback) - bot will not see other bots' messages")
else:
    print("Provide STRING_SESSION or BOT_TOKEN")
    raise SystemExit(1)

# parse watch list
watch_list = [w.strip() for w in WATCH_CHATS.split(",") if w.strip()]

async def post_text(text: str):
    headers = {"Content-Type": "application/json"}
    if WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = WEBHOOK_SECRET
    payload = {"text": text}
    async with ClientSession() as sess:
        try:
            async with sess.post(TARGET_WEBHOOK, json=payload, headers=headers, timeout=10) as resp:
                content = await resp.text()
                print("POST", resp.status, content[:200])
        except Exception as e:
            print("Webhook POST failed:", e)

@client.on(events.NewMessage())
async def handler(event):
    try:
        text = event.raw_text or (event.message.to_dict().get("message") if event.message else "") or ""
        text = text.strip()

        if not text:
            print("handler: empty text, skipping")
            return

        print("handler: posting text preview:", text[:200])
        await post_text(text) 

    except Exception as e:
        print("handler top-level error:", e)



async def main():
    try:
        if STRING_SESSION:
            await client.start()
        else:
            # bot fallback start with token if BOT_TOKEN provided
            await client.start(bot_token=BOT_TOKEN)
        print("Client started. Listening for new messages...")
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("Keyboard interrupt, stopping...")
    finally:
        try:
            await client.disconnect()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
