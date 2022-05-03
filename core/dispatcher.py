from django.conf import settings
from telegram import Bot
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, ConversationHandler, MessageHandler, Filters
from telegram.utils.request import Request

from core.handlers.admin_excel import admin_get_data, admin_users_excel, admin_exchanges_excel
from core.handlers.auth import start, set_language, uz_set, ru_set, uz, ru, full_name, phonenumber, edit_full_name
from core.handlers.core import home, setting, feedback, set_full_name, none, course_reserve, reserve, exchanges_history
from core.handlers.exchange import currency_exchange, give, get, exchange_from_card, exchange_to_card, exchange_retrieve, \
    exchange_create, exchange_save, enter_to_card, enter_from_card, enter_summa
from core.handlers.wallet import wallet, wallet_add, add_card, delete_card, delete_wallets, user_wallet_add
from core.helpers.variables import ContextData
from core.states import LANG, FULL_NAME, PHONE, SET_LANG, ALL, CARD_ADD, ENTER_SUMMA, ADD_FROM_CARD, ADD_TO_CARD


def entry_points() -> list:
    return [
        CommandHandler('start', start),
        CallbackQueryHandler(home, pattern="^(" + ContextData.HOME + ")$"),
        CallbackQueryHandler(set_language, pattern="^(setLang)$"),
        CallbackQueryHandler(setting, pattern="^(" + ContextData.SETTINGS + ")$"),
        CallbackQueryHandler(feedback, pattern="^(" + ContextData.FEEDBACK + ")$"),
        CallbackQueryHandler(set_full_name, pattern="^(setFullName)$"),
        CallbackQueryHandler(currency_exchange, pattern="^(exchange)$"),
        CallbackQueryHandler(uz_set, pattern="^(uz-set)$"),
        CallbackQueryHandler(ru_set, pattern="^(ru-set)$"),
        CallbackQueryHandler(uz, pattern='^(uz)$'),
        CallbackQueryHandler(ru, pattern='^(ru)$'),
        CallbackQueryHandler(none, pattern='^(none)$'),
        CallbackQueryHandler(course_reserve, pattern='^(course_reserve)$'),
        CallbackQueryHandler(reserve, pattern='^(reserve)$'),
        CallbackQueryHandler(give, pattern='give'),
        CallbackQueryHandler(get, pattern='get'),
        CallbackQueryHandler(wallet, pattern='^(' + ContextData.WALLET + ")$"),
        CallbackQueryHandler(wallet_add, pattern='addW'),
        CallbackQueryHandler(add_card, pattern='add_card'),
        CallbackQueryHandler(delete_card, pattern='delete_card'),
        CallbackQueryHandler(delete_wallets, pattern='delete_wallets'),
        CallbackQueryHandler(admin_get_data, pattern='^(data)$'),
        CallbackQueryHandler(admin_users_excel, pattern='^(users_excel)$'),
        CallbackQueryHandler(admin_exchanges_excel, pattern='^(exchanges_excel)$'),
        CallbackQueryHandler(exchange_from_card, pattern='^(exchange_from_card)$'),
        CallbackQueryHandler(exchange_to_card, pattern='^(exchange_to_card)$'),
        CallbackQueryHandler(exchange_retrieve, pattern='exchange-retrieve'),
        CallbackQueryHandler(exchange_create, pattern='^(exchange_create)$'),
        CallbackQueryHandler(exchange_save, pattern='^(exchange_save)$'),
        CallbackQueryHandler(exchanges_history, pattern='^(exchanges_history)$'),

    ]


def main():
    request = Request(connect_timeout=0.5, read_timeout=1.0)
    bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL)
    updater = Updater(bot=bot, use_context=True)

    all_handler = ConversationHandler(
        entry_points=entry_points(),
        states={
            LANG: entry_points() + [
                CallbackQueryHandler(start, pattern='start'),
            ],
            FULL_NAME: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, full_name),
            ],
            PHONE: [
                CommandHandler('start', start),
                MessageHandler(Filters.contact, phonenumber)
            ],
            ALL: entry_points(),
            SET_LANG: entry_points() + [
                CommandHandler('start', start),
                MessageHandler(Filters.text, edit_full_name),
            ],
            CARD_ADD: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, user_wallet_add),
                CallbackQueryHandler(wallet_add, pattern='addW'),
                CallbackQueryHandler(home, pattern="^(" + ContextData.HOME + ")$"),
            ],
            ENTER_SUMMA: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, enter_summa),
            ],
            ADD_FROM_CARD: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, enter_from_card),
            ],
            ADD_TO_CARD: [
                CommandHandler('start', start),
                MessageHandler(Filters.text, enter_to_card),
            ]
        },
        fallbacks=[]
    )

    updater.dispatcher.add_handler(all_handler)
    updater.start_polling()
    updater.idle()
