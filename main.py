import asyncio
from pyrogram import Client
import configparser
from bot_logic import setup_handlers


async def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config.getint("pyrogram", "api_id")
    api_hash = config.get("pyrogram", "api_hash")

    app = Client("VoronkaVebinar", api_id=api_id, api_hash=api_hash)
    
    await setup_handlers(app)

    await app.start()

    await asyncio.Event().wait()

asyncio.run(main())
