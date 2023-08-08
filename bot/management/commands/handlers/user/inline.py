from telebot.types import CallbackQuery

from bot.management.commands.decorators import is_channel
from bot.management.commands.handlers.user.start import start_handler
from bot.management.commands.loader import bot


@bot.callback_query_handler(func=lambda msg: msg.data == "confirm")
@is_channel
def confirm_handler(msg: CallbackQuery):
    user_id = msg.from_user.id
    bot.delete_message(user_id, message_id=msg.message.message_id)
    start_handler(msg)
