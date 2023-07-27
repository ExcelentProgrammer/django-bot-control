from django.conf import settings
from telebot import TeleBot

bot = TeleBot(settings.BOT_TOKEN)
