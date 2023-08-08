from threading import Thread

from telebot.types import Message

from bot.management.commands.loader import bot, lang, config
from bot.management.commands.utils.downloader import Downloader
from bot.tasks import download_task


@bot.message_handler(func=lambda msg: Downloader.is_url(msg.text))
def download_handler(msg: Message):
    user_id = msg.chat.id
    url = msg.text
    if not Downloader.is_url(url):
        bot.send_message(msg.chat.id, '''😔 Siz yuborgan xabardan havola topa olmadim.
Menga havola yuboring 👌''')
        return

    res = Downloader.exists_video(url)

    if res.get("status"):
        bot.send_video(user_id, res.get("file_id"), caption=lang.get("caption", me=config.get("me")))
        return

    message_id = bot.send_message(user_id, "⏳").message_id

    task = Thread(target=download_task, kwargs=dict(url=url, user_id=user_id, message_id=message_id))
    task.start()
