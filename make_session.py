# make_session.py (fixed)
import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    print("Please set API_ID and API_HASH in .env first.")
    raise SystemExit(1)

API_ID = int(API_ID)
API_HASH = str(API_HASH)

async def gen_session():
    print("== Telethon login to generate STRING_SESSION ==")
    print("If you have 2FA you will be asked for the password.")
    input("Press Enter to continue...")

    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        me = await client.get_me()
        print("Logged in as:", getattr(me, "username", repr(me)))
        s = client.session.save()
        print("\n===== COPY THIS STRING (STRING_SESSION) AND PUT INTO .env =====\n")
        print(s)
        print("\n===== END =====\n")

if __name__ == "__main__":
    asyncio.run(gen_session())
