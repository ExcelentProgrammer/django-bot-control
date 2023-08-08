from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.management.commands.loader import bot, lang
from sponsors.models import Sponsors


def is_channel(func):
    def decerator(msg):
        user_id = msg.from_user.id

        channels = Sponsors.objects.all()

        left_channels = []
        for channel in channels:
            res = bot.get_chat_member(chat_id=channel.link, user_id=msg.from_user.id).status
            if res in ['administrator', "creator", "member"]:
                continue
            else:
                left_channels.append(channel)
        if len(left_channels) > 0:
            keywords = InlineKeyboardMarkup()
            for left_channel in left_channels:
                keywords.add(InlineKeyboardButton(text=left_channel.name,
                                                  url="https://t.me/{}".format(left_channel.username.replace("@", ""))))

            keywords.add(InlineKeyboardButton(text=lang.get("confirm"), callback_data="confirm"))
            try:
                if not hasattr(msg,"data"):
                    bot.send_message(user_id, lang.get("subscribe"), reply_markup=keywords)
                else:
                    bot.answer_callback_query(msg.id,lang.get("not_subscribe"))
            except Exception as e:
                print(e)

        else:
            return func(msg)

    return decerator
    