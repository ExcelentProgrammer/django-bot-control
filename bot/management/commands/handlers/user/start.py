from telebot.types import Message

from bot.management.commands import keyboards
from bot.management.commands.decorators import is_channel
from bot.management.commands.loader import bot, lang
from bot.models import User


@bot.message_handler(commands=['start'])
@is_channel
def start_handler(msg: Message):
    user_id = msg.from_user.id
    check = User.objects.filter(user_id=user_id)

    if not check.exists():
        User.objects.create(user_id=user_id)

    bot.send_message(user_id, lang.get("start"), reply_markup=keyboards.inline.add_group)
