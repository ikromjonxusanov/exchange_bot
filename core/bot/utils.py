from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from core.bot.helpers import get_bot_user, get_keyboard, Message, ContextData
from core.decorators import login_user_query


@login_user_query
def home(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(text=Message(user.lang).HOME, parse_mode="HTML", reply_markup=get_keyboard(user.lang))


@login_user_query
def setting(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="📝 Tilni o'zgartirish" if user.lang == 'uz' else "📝 Изменить язык",
                callback_data='setLang'
            ),
        ],
        [
            InlineKeyboardButton(
                text="✏ F.I.SH o'zgartirish" if user.lang == 'uz' else "✏ Изменение Ф.И.О.",
                callback_data='data'
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga" if user.lang == 'uz' else "🔙 Назад",
                callback_data=ContextData.HOME
            ),
        ]
    ])
    query.edit_message_text(
        text="⚙️ Sozlamalar" if user.lang == 'uz' else "⚙️ Настройки",
        parse_mode="HTML",
        reply_markup=keyboard
    )
