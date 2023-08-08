import asyncio

from django.conf import settings
from telebot import TeleBot

from utils.config import Config
from utils.language import Language




bot = TeleBot(settings.BOT_TOKEN)
lang = Language("uz")
config = Config()
