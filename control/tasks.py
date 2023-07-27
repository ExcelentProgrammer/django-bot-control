from django.conf import settings
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.management.commands.loader import bot
from bot.models import User
from control.models import Tasks


def sendMessageTask(message, type, file, task, keyboards=None):
    users = User.objects.all()
    kbs = None

    if keyboards is not None:
        kbs = InlineKeyboardMarkup()
        for keyboard in keyboards:
            kbs.add(InlineKeyboardButton(text=keyboard['title'], url=keyboard['url']))

    if type == "image":
        message_id = bot.send_photo(settings.ADMIN, photo=file, caption=message, reply_markup=kbs).message_id
    elif type == "video":
        message_id = bot.send_video(settings.ADMIN, video=file, caption=message, reply_markup=kbs).message_id
    elif type == "audio":
        message_id = bot.send_audio(settings.ADMIN, audio=file, caption=message, reply_markup=kbs).message_id
    elif type == "text":
        message_id = bot.send_message(settings.ADMIN, text=message, reply_markup=kbs).message_id
    else:
        return

    task = Tasks.objects.get(id=task)
    task.total = users.count()
    task.save()

    i = 1

    done = 1
    error = 0

    for user in users:
        if str(user.user_id) != str(settings.ADMIN):
            try:
                bot.copy_message(user.user_id, settings.ADMIN, message_id=message_id, reply_markup=kbs)
                done += 1
            except Exception as e:
                print(e)
                error += 1
            if i % 5 == 0:
                task.done = done
                task.error = error
                task.save()
    task.success = True
    task.done = done
    task.error = error
    task.save()
