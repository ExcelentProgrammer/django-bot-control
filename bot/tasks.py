import os
from uuid import uuid4

import wget

from bot.management.commands import keyboards
from bot.management.commands.loader import bot, config, lang
from bot.management.commands.utils.downloader import Downloader
from bot.models import Videos


def download_task(url, user_id, message_id):
    check = Downloader.check_url(url)
    try:
        if check == "instagram":
            res = Downloader.instagram(url)
            bot.delete_message(user_id, message_id)
            file_id = bot.send_video(user_id, res['url'],
                                     caption='''📥 @{} bilan yuklab olindi'''.format(config.get("me")),
                                     reply_markup=keyboards.inline.share)
        elif check == "tiktok":
            res = Downloader.tiktok(url)
            bot.delete_message(user_id, message_id)
            file_id = bot.send_video(user_id, res['url'],
                                     caption=lang.get("caption", config.get('me')),
                                     reply_markup=keyboards.inline.share)
        elif check == "youtube":
            res = Downloader.youtube(url)
            bot.delete_message(user_id, message_id)

            if not res['success']:
                bot.send_message(user_id, res['message'])
                return
            file_id = bot.send_video(user_id, video=open(res['filepath'], "rb"),
                                     caption=lang.get("caption", config.get('me')),
                                     reply_markup=keyboards.inline.share)

            os.remove(res['filepath'])
        elif check == "facebook":
            res = Downloader.facebook(url)
            bot.delete_message(user_id, message_id)
            if not res['success']:
                bot.send_message(user_id, "😔 Afsuski yuklash davomida xatolik yuz berdi, qayta urinib ko'ring!")
                return
            file_id = bot.send_video(user_id, video=open(res['filepath'], "rb"),
                                     caption=lang.get("caption", config.get('me')),
                                     reply_markup=keyboards.inline.share)
            os.remove(res['filepath'])
        file_id = file_id.video.file_id

        Videos.objects.create(file_id=file_id, url=url)

        return "success"
    except Exception as e:
        file_path = "media/temp/{}.mp4".format(uuid4())

        try:
            if str(e) != "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: failed to get HTTP URL content":
                res = wget.download(res['url'], file_path)
                bot.send_video(user_id, video=open(res, "rb"),
                               caption='''📥 @{} bilan yuklab olindi'''.format(config.get("me")), timeout=60)
                os.remove(file_path)
            return
        except Exception as e:
            print(e)
        bot.send_message(user_id, lang.get("send_video_error"))
        return "error"
