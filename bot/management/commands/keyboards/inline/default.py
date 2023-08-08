from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.management.commands.loader import lang, config

# guruhga qo'shish
add_group = InlineKeyboardMarkup()
add_group.add(
    InlineKeyboardButton(text=lang.get("add_group", "Guruhga qo'shish"),
                         url="https://t.me/{}?startgroup=new".format(config.get("me"))))

share = InlineKeyboardMarkup()
share.add(InlineKeyboardButton(text=lang.get("share"),
                               url="https://t.me/share/url?url=https://t.me/{}".format(config.get("me"))))
