from django.core.management import BaseCommand
from telebot.custom_filters import StateFilter

from .loader import bot

from . import states
from . import handlers

from .pbot import *


class Command(BaseCommand):
    help = "django bot run"

    def handle(self, *args, **kwargs):
        bot.add_custom_filter(StateFilter)
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
