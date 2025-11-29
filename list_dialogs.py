# list_dialogs.py
import asyncio, os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
load_dotenv()
API_ID=int(os.getenv("API_ID"))
API_HASH=os.getenv("API_HASH")
S=os.getenv("STRING_SESSION")
async def main():
    client = TelegramClient(StringSession(S), API_ID, API_HASH)
    await client.start()
    dialogs = await client.get_dialogs(limit=200)
    for d in dialogs:
        c = d.entity
        print("id:", getattr(c,'id',None),"title/username:", getattr(c,'title',None) or getattr(c,'username',None), "is_channel", getattr(c,'broadcast',False))
    await client.disconnect()
asyncio.run(main())
