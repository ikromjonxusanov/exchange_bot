import re

from django.db import transaction
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from core.decorators import login_user, login_user_query
from core.handlers.core import home
from core.helpers.keyboards import wallet_add_keyboard
from core.helpers.variables import get_bot_user, ButtonText, ContextData, get_text_wallet, Message, wallet_add_or_change
from core.models import Currency, Wallet
from core.states import ALL, CARD_ADD


@login_user_query
def wallet(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    currencies = Currency.objects.all().values('id', 'name', "validate")
    keyboard = []
    tmp_b = []
    keyboard.append([
        InlineKeyboardButton(text=ButtonText(user.lang).back, callback_data=ContextData.HOME),
    ])
    for c in currencies:
        tmp_b.append(InlineKeyboardButton(c['name'], callback_data=f"addW/{c['id']}"))
        if len(tmp_b) == 2:
            keyboard.append(tmp_b)
            tmp_b = []
    else:
        keyboard.append(tmp_b)
    if Wallet.objects.filter(user=user).count() > 0:
        keyboard.append([
            InlineKeyboardButton(text=ButtonText(user.lang).delete, callback_data='delete_wallets'),
        ])

    query.edit_message_text(
        text=Message(user.lang).wallet + get_text_wallet(user),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@login_user_query
def delete_wallets(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    with transaction.atomic():
        Wallet.objects.filter(user=user).delete()
        query.answer(show_alert=True, text='✅ ' + "O'chirildi" if user.lang == 'uz' else "Удалено")
        home(update, context)


@login_user_query
def wallet_add(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    currency = Currency.objects.get(id=int(query.data.split('/')[1]))
    w = Wallet.objects.filter(user=user, currency=currency).first()
    resp = w.number if w else "Bo'sh" if user.lang == 'uz' else "Пустой"
    text = f"💳 <b>{currency.name}</b>: <i>{resp}</i>"
    keyboard = [
        [
            InlineKeyboardButton(
                wallet_add_or_change(not bool(w), user.lang),
                callback_data=f'add_card/{currency.id}')
        ],
        [
            InlineKeyboardButton(ButtonText(user.lang).back, callback_data=ContextData.WALLET),
        ],
        [
            InlineKeyboardButton(ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
        ]
    ]
    if w:
        keyboard[0].append(
            InlineKeyboardButton(
                ButtonText(user.lang).delete_wallet,
                callback_data=f'delete_card/{currency.id}')
        )
    query.edit_message_text(
        text=text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ALL


@login_user_query
def add_card(update: Update, context: CallbackContext):
    query = update.callback_query
    cid = int(query.data.split("/")[1])
    user = get_bot_user(query.from_user.id)
    try:
        currency = Currency.objects.get(id=cid)
        text = f"✏ {currency.name} hisob raqamingizni kiriting\nDefault: {currency.example}"
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(ButtonText(user.lang).cancel, callback_data=f"addW/{currency.id}"),
            ],
            [
                InlineKeyboardButton(ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
            ]
        ])
        query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
        context.user_data[f"{user.tg_id}"] = {
            "cid": currency.id,
            "msgid": query.message.message_id
        }
        return CARD_ADD
    except Currency.DoesNotExist:
        txt = ("🛑 Tanlanga valyuta mavjud emas iltimos /start bering va qaytadan ishlating"
               if user.lang == 'uz' else
               "🛑 Выбранная валюта недоступна Пожалуйста, дайте /start и используйте снова")
        query.answer(show_alert=True, text=txt)


@login_user_query
def delete_card(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    with transaction.atomic():
        cur = Currency.objects.filter(id=int(query.data.split('/')[1])).first()
        Wallet.objects.get(currency=cur, user=user).delete()
        query.answer(show_alert=True, text='✅ ' + "O'chirildi" if user.lang == 'uz' else "Удалено")

        wallet(update, context)


@login_user
def user_wallet_add(update: Update, context: CallbackContext):
    number = update.message.text
    user = get_bot_user(update.message.from_user.id)
    data = context.user_data.get(f'{user.tg_id}', {'cid': None, 'msgid': None})
    if data.get('msgid') is not None:
        context.bot.deleteMessage(chat_id=update.message.from_user.id,
                                  message_id=data['msgid'])
        del data['msgid']
    if data is not None:
        cid = data['cid']
        currency = Currency.objects.get(id=cid)
        validate = True
        if currency.validate:
            if not re.fullmatch(currency.validate, number):
                validate = False
        if validate:
            with transaction.atomic():
                w, _ = Wallet.objects.get_or_create(user=user, currency=currency)
                w.number = number
                w.save()
                keyboard = wallet_add_keyboard(user.lang)
                update.message.reply_html("✅ Kartani saqlandi" if user.lang == 'uz' else "✅ Карта сохранена",
                                          reply_markup=keyboard)
                return ALL
        else:
            txt = "Quyidagi tarzda kiriting" if user.lang == 'uz' else "Введите следующим образом"
            update.message.reply_html(f"<pre>{currency.example}</pre>\n" + txt)
