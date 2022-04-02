from telegram import Update
from telegram.ext import CallbackContext
from core.bot.auth import start
from core.bot.helpers import get_bot_user


def login_user_query(view_func):
    def wrapper(update: Update, context: CallbackContext):
        query = update.callback_query
        user_id = query.from_user.id
        user = get_bot_user(user_id)
        if user.is_active:
            return view_func(update, context)
        else:
            start(update, context, user_id)

    return wrapper


def login_user(view_func):
    def wrapper(update: Update, context: CallbackContext):
        user = get_bot_user(update.message.from_user.id)
        if user.is_active:
            return view_func(update, context)
        else:
            start(update, context)

    return wrapper

