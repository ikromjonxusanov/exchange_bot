from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import CallbackContext
from core.bot.helpers import get_bot_user, get_keyboard, Message

LANG = 1
FULL_NAME = 2
PHONE = 3
ALL = 4


def start(update: Update, context: CallbackContext, pk=None):
    # print(update.message)
    if pk is None:
        user_id = update.message.from_user.id
    else:
        user_id = pk
    user = get_bot_user(user_id)
    if user.is_active:
        update.message.reply_html(Message(user.lang).HOME,
                                  reply_markup=get_keyboard(lang=user.lang, admin=user.is_admin))
        return ALL
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data='uz'),
            InlineKeyboardButton(text="🇷🇺 русский язык", callback_data="ru")
        ]
    ])
    if pk is None:
        update.message.reply_html("Tilni tanlang👇\n-----------\nВыберите язык👇", reply_markup=keyboard)
    else:
        update.callback_query.edit_message_text("Tilni tanlang👇\n-----------\nВыберите язык👇", reply_markup=keyboard)
    return LANG


def set_lang(lang, user_id):
    user = get_bot_user(tg_id=user_id)
    user.lang = lang
    user.save()


def uz(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.message.delete()
    set_lang('uz', query.from_user.id)
    query.message.reply_html("To'liq ismingizni kiriting")
    return FULL_NAME


def ru(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.message.delete()
    set_lang('ru', query.from_user.id)
    query.message.reply_html("Введите ваше полное имя")
    return FULL_NAME


def full_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user = get_bot_user(user_id)
    user.full_name = update.message.text
    user.save()
    if user.lang == 'uz':
        btn_text = '📲 Kontaktni jo\'natish'
        text = "📲 Telefon nomeringizni yuboring"
    else:
        btn_text = '📲 Отправить контакт'
        text = "📲 Отправьте свой номер телефона"

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(btn_text, request_contact=True)]],
                                       resize_keyboard=True, selective=True)
    update.message.reply_html(text, reply_markup=reply_markup)
    return PHONE


def uz_set(update: Update, context: CallbackContext):
    query = update.callback_query
    set_lang(lang='uz', user_id=query.from_user.id)
    query.edit_message_text(Message("uz").HOME, parse_mode="HTML", reply_markup=get_keyboard('uz'))


def ru_set(update: Update, context: CallbackContext):
    query = update.callback_query
    set_lang(lang='ru', user_id=query.from_user.id)
    query.edit_message_text(Message("ru").HOME, parse_mode="HTML", reply_markup=get_keyboard('ru'))


def set_language(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data='uz-set'),
            InlineKeyboardButton(text="🇷🇺 русский язык", callback_data="ru-set")
        ]
    ])
    query.message.delete()
    query.message.reply_html('Tilni tanlang👇' if user.lang == 'uz' else 'Выберите язык👇', reply_markup=keyboard)


def phonenumber(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user = get_bot_user(user_id)
    user.phone = update.message.contact.phone_number
    user.is_active = True
    user.save()
    update.message.reply_html(text="🤖 Bot dan muvaffaqiyatlili ro‘yxatdan o‘tdingiz!!! ✅",
                              reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    update.message.reply_html(Message(user.lang).HOME, reply_markup=get_keyboard(user.lang, admin=user.is_admin))
    return ALL


def edit_full_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user = get_bot_user(user_id)
    user.full_name = update.message.text
    user.save()
    update.message.delete()
    update.message.reply_html(Message(user.lang).HOME, reply_markup=get_keyboard(user.lang, admin=user.is_admin))
    return ALL
