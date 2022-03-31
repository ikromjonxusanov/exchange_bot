from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from core.bot.helpers import get_bot_user, get_keyboard, Message
from core.decorators import login_user_query


@login_user_query
def home(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(text="", parse_mode="HTML", reply_markup=get_keyboard(user.lang))


@login_user_query
def settings(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = [
        [
            InlineKeyboardButton(text="✏ Tilni o'zgartirish" if user.lang == 'uz' else "✏ Изменить язык"),
            InlineKeyboardButton(text=" " if user.lang == 'uz' else "✏ Изменить язык"),
        ]
    ]
    query.edit_message_text(text="", parse_mode="HTML", reply_markup=get_keyboard(user.lang))