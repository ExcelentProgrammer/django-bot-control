from pyrogram import Client

from config import settings

app = Client(name="bot.session", bot_token=settings.BOT_TOKEN, api_id="7878494",
             api_hash="3b7035773fde7b903fa430a6f1540e32")


async def send_message(*args, **kwargs):
    async with app:
        await app.send_message(*args, **kwargs)


async def send_video(*args, **kwargs):
    async with app:
        await app.send_video(*args, **kwargs)
