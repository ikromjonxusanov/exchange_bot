from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from core.helpers.variables import get_bot_user, Message, ContextData, ButtonText
from core.decorators import login_user_query
from core.helpers.keyboards import get_course_reserve, get_reserve, get_keyboard
from core.states import ALL, SET_LANG


@login_user_query
def home(update: Update, context: CallbackContext, delete: bool = True):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    if delete:
        query.message.delete()
    query.message.reply_html(text=Message(user.lang).HOME,
                             reply_markup=get_keyboard(user.lang, admin=user.is_admin))
    return ALL


@login_user_query
def setting(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).set_lang,
                callback_data='setLang'
            ),
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).set_full_name,
                callback_data='setFullName'
            ),
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).back,
                callback_data=ContextData.HOME
            ),
        ]
    ])
    query.edit_message_text(
        text=Message(user.lang).settings,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME),
    ]])
    query.edit_message_text(
        text=Message(user.lang).feedback,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def set_full_name(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(update.callback_query.from_user.id)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME),
    ]])
    query.edit_message_text(
        text=Message(user.lang).set_full_name,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    return SET_LANG


def none(update: Update, context: CallbackContext):
    query = update.callback_query


@login_user_query
def course_reserve(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=ButtonText(user.lang).reserve, callback_data=ContextData.RESERVE)
        ],
        [
            InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME),
        ]
    ])
    query.edit_message_text(
        text=get_course_reserve(user.lang),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def reserve(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=ButtonText(user.lang).course, callback_data='course_reserve')
        ],
        [
            InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME),
        ]
    ])
    query.edit_message_text(
        text=get_reserve(user.lang),
        parse_mode="HTML",
        reply_markup=keyboard
    )
