from django.conf import settings
from django.core.management import BaseCommand
from telegram import Bot
from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request

from core.bot.auth import start, uz, ru, full_name, phonenumber, set_language, uz_set, ru_set
from core.bot.utils import setting, home

LANG = 1
FULL_NAME = 2
PHONE = 3
ALL = 4


class Command(BaseCommand):
    help = "Telegram bot"

    def entry_points(self) -> list:
        return [
            CommandHandler('start', start),
            CallbackQueryHandler(home, pattern='home'),
        ]

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
        updater = Updater(bot=bot, use_context=True)

        all_handler = ConversationHandler(
            entry_points=self.entry_points(),
            states={
                LANG: [
                    CallbackQueryHandler(start, pattern='start'),
                    CallbackQueryHandler(uz, pattern='^(uz)$'),
                    CallbackQueryHandler(ru, pattern='^(ru)$')
                ],
                FULL_NAME: [
                    CommandHandler('start', start),
                    MessageHandler(Filters.text, full_name),
                ],
                PHONE: [
                    CommandHandler('start', start),
                    MessageHandler(Filters.contact, phonenumber)
                ],
                ALL: self.entry_points() + [
                    CallbackQueryHandler(set_language, pattern="setLang"),
                    CallbackQueryHandler(setting, pattern="settings"),
                    CallbackQueryHandler(uz_set, pattern="uz-set"),
                    CallbackQueryHandler(ru_set, pattern="ru-set")
                    # MessageHandler(Filters.location, location),
                ],

            },
            fallbacks=[]
        )

        updater.dispatcher.add_handler(all_handler)
        updater.start_polling()
        updater.idle()
