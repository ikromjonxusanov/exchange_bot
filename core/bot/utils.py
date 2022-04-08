from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from core.bot.helpers import get_bot_user, get_keyboard, Message, ContextData, ButtonText
from core.decorators import login_user_query
from core.helpers import get_course_reserve, exchange_cancel_back_buttons, get_reserve
from core.models import Currency, AcceptableCurrency

SET_LANG = 5


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
    query.answer()
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
    query.answer()
    query.edit_message_text(
        text=Message(user.lang).set_full_name,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    return SET_LANG


@login_user_query
def currency_exchange(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = get_bot_user(query.from_user.id)
    keyboard = []
    currencies = Currency.objects.all()
    for c in currencies:
        keyboard.append([
            InlineKeyboardButton(text="🔷" + c.name, callback_data=f'give/{c.id}'),
            InlineKeyboardButton(text="🔶" + c.name, callback_data=f'get/{c.id}')
        ])
    keyboard.append([InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME)])
    query.edit_message_text(
        text=Message(user.lang).exchange,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@login_user_query
def give(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = get_bot_user(query.from_user.id)
    keyboard = []
    pk = int(query.data.split('/')[1])
    currency = Currency.objects.get(id=pk)
    currencies = Currency.objects.all()
    acceptablecurrencies = AcceptableCurrency.objects.filter(currency=currency).first()
    acceptable = acceptablecurrencies.acceptable.all()
    for c in currencies:
        keyboard.append([
            InlineKeyboardButton(text="🔷" + c.name, callback_data=f'give/{c.id}'),
            InlineKeyboardButton(text="➖", callback_data=f'none')
        ])
    for i in range(len(acceptable)):
        keyboard[i][1] = InlineKeyboardButton(text="🔶" + acceptable[i].name, callback_data=f'none')

    keyboard.extend(
        exchange_cancel_back_buttons(user.lang)
    )

    try:
        query.edit_message_text(
            text=Message(user.lang).exchange,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        print("No edit text")


@login_user_query
def get(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = []
    pk = int(query.data.split('/')[1])
    query.answer()
    currency = Currency.objects.get(id=pk)
    currencies = Currency.objects.all()
    acceptablecurrencies = AcceptableCurrency.objects.filter(currency=currency).first()
    acceptable = acceptablecurrencies.acceptable.all()
    for c in currencies:
        keyboard.append([
            InlineKeyboardButton(text="➖", callback_data=f'none'),
            InlineKeyboardButton(text="🔶" + c.name, callback_data=f'get/{c.id}'),
        ])
    for i in range(len(acceptable)):
        keyboard[i][0] = InlineKeyboardButton(text="🔷" + acceptable[i].name, callback_data=f'none')
    keyboard.extend(
        exchange_cancel_back_buttons(user.lang)
    )
    try:
        query.edit_message_text(
            text=Message(user.lang).exchange,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        print("No edit text")


def none(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


@login_user_query
def course_reserve(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.answer()
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
    query.answer()
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
