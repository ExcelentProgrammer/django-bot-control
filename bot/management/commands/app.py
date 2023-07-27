from django.core.management import BaseCommand

from .loader import bot

from . import handlers


class Command(BaseCommand):
    help = "django bot run"

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
