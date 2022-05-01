import datetime
import random
import string

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from common.service import get_user_for_excel, get_exchange_for_excel
from core.decorators import admin_user_query
from core.helpers.variables import get_bot_user, ButtonText, Message, ContextData
from core.models import Excel


def generate_filename():
    txt = "{:%Y}-{:%M}-{:%d}-".format(datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())
    return txt + "".join([random.choice(string.ascii_lowercase) for _ in range(40)])


@admin_user_query
def admin_get_data(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = [
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).get_users_for_excel_button, callback_data='users_excel'
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).get_changes_for_excel_button, callback_data='exchanges_excel'
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(user.lang).back_home, callback_data=ContextData.HOME
            )
        ]
    ]
    query.edit_message_text(
        text=Message(user.lang).data_excel,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@admin_user_query
def admin_users_excel(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(
        text="⏳ Ma'lumotlar <b>excel</b> formatga o'tkazilmoqda iltimos kuting!",
        parse_mode='HTML'
    )
    excel = Excel(
        name=f'Users get data for excel message id -> {query.message.message_id}',
        from_user=user
    )
    file = get_user_for_excel(generate_filename())
    excel.file = file
    excel.save()
    try:
        query.message.reply_document(
            document=open("uploads/" + str(excel.file), 'rb'),
            filename="Customers.xlsx",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text=ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
                ]
            ])
        )
        query.message.delete()
    except FileNotFoundError:
        query.edit_message_text(
            text=Message(user.lang).get_data_excel_error,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="👨🏻‍💻 Dasturchiga murojaat qilish",
                                         url="https://t.me/ikromjonxusanov"),
                ],
                [
                    InlineKeyboardButton(text=ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
                ]
            ])
        )


@admin_user_query
def admin_exchanges_excel(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(
        text="⏳ Ma'lumotlar <b>excel</b> formatga o'tkazilmoqda iltimos kuting!",
        parse_mode='HTML'
    )
    excel = Excel(
        name=f'Exchanges get data for excel message id -> {query.message.message_id}',
        from_user=user
    )
    file = get_exchange_for_excel(generate_filename())
    excel.file = file
    excel.save()
    try:
        query.message.reply_document(
            document=open("uploads/" + str(excel.file), 'rb'),
            filename="Exchanges.xlsx",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text=ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
                ]
            ])
        )
        query.message.delete()
    except FileNotFoundError or ValueError:
        query.edit_message_text(
            text=Message(user.lang).get_data_excel_error,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="👨🏻‍💻 Dasturchiga murojaat qilish",
                                         url="https://t.me/ikromjonxusanov"),
                ],
                [
                    InlineKeyboardButton(text=ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
                ]
            ])
        )
