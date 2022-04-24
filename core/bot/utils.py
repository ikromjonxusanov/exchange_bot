import re
import random as rn
import datetime as d
import string
from django.db import transaction
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from common.service import get_user_for_excel
from core.bot.helpers import get_bot_user, get_keyboard, Message, ContextData, ButtonText, get_text_wallet, \
    get_exchange_text
from core.decorators import login_user_query, login_user, admin_user_query
from core.helpers import get_course_reserve, exchange_cancel_back_buttons, get_reserve
from core.models import Currency, AcceptableCurrency, Wallet, Excel, CurrencyMinBuy, Exchange

ALL = 4
SET_LANG = 5
CARD_ADD = 6
ENTER_SUMMA = 7
ADD_FROM_CARD = 8
ADD_TO_CARD = 9
wallet_name = dict()


def generate_filename():
    txt = "{:%Y}-{:%M}-{:%d}-".format(d.datetime.now(), d.datetime.now(), d.datetime.now(), d.datetime.now())
    return txt + "".join([rn.choice(string.ascii_lowercase) for _ in range(40)])


@login_user_query
def home(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
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


@login_user_query
def currency_exchange(update: Update, context: CallbackContext):
    query = update.callback_query
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
    user = get_bot_user(query.from_user.id)
    keyboard = []
    pk = int(query.data.split('/')[1])
    currency = Currency.objects.get(id=pk)
    currencies = Currency.objects.all()
    acceptablecurrencies = AcceptableCurrency.objects.filter(currency=currency).first()
    acceptable = acceptablecurrencies.acceptable.all()
    for c in currencies:
        data = [
            InlineKeyboardButton(text="🔷" + c.name, callback_data=f'give/{c.id}'),
            InlineKeyboardButton(text="➖", callback_data=f'none')
        ]
        if c.id == pk:
            data[0] = InlineKeyboardButton(text="✅" + c.name, callback_data=f'give/{c.id}')
        keyboard.append(data)
    for i in range(len(acceptable)):
        keyboard[i][1] = InlineKeyboardButton(text="🔶" + acceptable[i].name,
                                              callback_data=f'exchange-get/{pk}/{acceptable[i].id}')

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
        data = [
            InlineKeyboardButton(text="➖", callback_data=f'none'),
            InlineKeyboardButton(text="🔶" + c.name, callback_data=f'get/{c.id}'),
        ]
        if c.id == pk:
            data[1] = InlineKeyboardButton(text="✅" + c.name, callback_data=f'get/{c.id}')
        keyboard.append(data)
    for i in range(len(acceptable)):
        keyboard[i][0] = InlineKeyboardButton(text="🔷" + acceptable[i].name,
                                              callback_data=f'exchange-get/{acceptable[i].id}/{pk}')
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
def exchange_get(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    from_card = Currency.objects.filter(id=int(query.data.split('/')[1])).first()
    to_card = Currency.objects.filter(id=int(query.data.split('/')[2])).first()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=ButtonText(user.lang).give + from_card.name, callback_data="exchange_from_card")],
        [InlineKeyboardButton(text=ButtonText(user.lang).get + to_card.name, callback_data="exchange_to_card")],
        [InlineKeyboardButton(text=ButtonText(user.lang).cancel, callback_data=ContextData.HOME)],
    ])
    context.user_data["from_card"] = from_card
    context.user_data["to_card"] = to_card
    query.edit_message_text(text=get_exchange_text(user.lang, from_card, to_card),
                            parse_mode="HTML",
                            reply_markup=keyboard)


@login_user_query
def exchange_from_card(update: Update, context: CallbackContext):
    query = update.callback_query
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    context.user_data['code'] = from_card
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    if minbuy:
        code = from_card.code
        if from_card.code == 'UZS':
            code = 'So`m'
        msg = f"⬆ ️Berish miqdorini <b>{from_card.name}</b>da kiriting:\n\n" \
              f"Minimal:  <i>{minbuy.min_buy_f}</i> {code}\n" \
              "Bekor qilish uchun /start deb yozing."

        query.edit_message_text(msg, parse_mode="HTML")
        return ENTER_SUMMA
    else:
        query.answer(show_alert=True, text="❌ Ma'lumot to'ldirilmagan")
        currency_exchange(update, context)


@login_user_query
def exchange_to_card(update: Update, context: CallbackContext):
    query = update.callback_query
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    context.user_data['code'] = to_card
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    if minbuy:
        code = to_card.code
        if to_card.code == 'UZS':
            code = 'So`m'
        msg = f"⬇ Olish miqdorini <b>{to_card.name}</b>da kiriting:\n\n" \
              f"Minimal:  <i>{minbuy.min_buy_t}</i> {code}\n" \
              "Bekor qilish uchun /start deb yozing."
        query.edit_message_text(msg, parse_mode="HTML")
        return ENTER_SUMMA
    else:
        query.answer(show_alert=True, text="❌ Ma'lumot to'ldirilmagan")
        currency_exchange(update, context)


@login_user
def enter_summa(update: Update, context: CallbackContext):
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    minbuy_value = minbuy.min_buy_f
    card = from_card
    try:
        if minbuy.to_card == context.user_data['code']:
            minbuy_value = minbuy.min_buy_t
            card = to_card
        print(minbuy_value, minbuy, minbuy.id,
              from_card, to_card)
        summa = float(update.message.text)
        if minbuy_value <= summa:
            update.message.reply_html(
                "<i>Siz to‘lov qilmoqchi bo‘lgan</i>"
                f"\n\n<b>{from_card.name}</b> raqamni kiriting:"
                f"\nMisol uchun: <i>({from_card.example})</i>"
            )
            context.user_data['exchange'] = {'summa': summa}
            return ADD_FROM_CARD
        else:
            code = card.code
            if card.code == 'UZS':
                code = 'So`m'
            update.message.reply_html(
                f"Minimal:  <i>{minbuy_value}</i> {code}\n"
                "Bekor qilish uchun /start deb yozing."
            )
    except ValueError:
        code = card.code
        if card.code == 'UZS':
            code = 'So`m'
        update.message.reply_html(
            f"Minimal:  <i>{minbuy_value}</i> {code}\n"
            "Bekor qilish uchun /start deb yozing."
        )


@login_user
def enter_from_card(update: Update, context: CallbackContext):
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    if re.fullmatch(from_card.validate, update.message.text) is not None:
        update.message.reply_html(
            "<i>Siz to‘lov qilmoqchi bo‘lgan</i>"
            f"\n\n<b>{to_card.name}</b> raqamni kiriting:"
            f"\nMisol uchun: <i>({to_card.example})</i>")
        context.user_data['exchange']['from_card'] = update.message.text
        return ADD_TO_CARD
    else:
        update.message.reply_html(
            f"<b>{from_card.name}</b> raqamni kiriting:"
            f"\nMisol uchun: <i>({from_card.example})</i>")


@login_user
def enter_to_card(update: Update, context: CallbackContext):
    user = get_bot_user(update.message.from_user.id)
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    summa = context.user_data['exchange']['summa']
    if re.fullmatch(to_card.validate, update.message.text) is not None:
        Exchange.objects.create(
            user=user,
            from_card=context.user_data['exchange']['from_card'],
            to_card=update.message.text,
            summa=summa
        )
        if str(from_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == from_card:
            price = "%.2f" % (float(summa) / to_card.sell)
        elif str(from_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == to_card:
            price = "%.2f" % (float(summa) * to_card.sell)
        elif str(to_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == from_card:
            price = "%.2f" % (float(summa) * from_card.buy)
        elif str(to_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == to_card:
            price = "%.2f" % (float(summa) / from_card.buy)
        else:
            price = None
        update.message.reply_html(
            "🔖Sizning almashuv:\n\n"
            f"🔀:{from_card} ➡️ {to_card}"
            f"\n {summa} -> {price}"
        )
    else:
        update.message.reply_html(
            "❌"
        )


def none(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer(show_alert=True, text="🛑 None")


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
                ButtonText(user.lang).wallet_add_or_change(not bool(w), user.lang),
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
        wallet_name[f"{user.tg_id}"] = {
            "cid": currency.id,
            "msgid": query.message.message_id
        }
        return CARD_ADD
    except Currency.DoesNotExist:
        query.answer("🛑 Tanlanga valyuta mavjud emas iltimos /start bering va qaytadan ishlating")


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
    data = wallet_name.get(f'{user.tg_id}', {'cid': None, 'msgid': None})
    if data.get('msgid') is not None:
        context.bot.deleteMessage(chat_id=update.message.from_user.id,
                                  message_id=data['msgid'])
        del data['msgid']
    if data is not None:
        cid = data['cid']
        currency = Currency.objects.get(id=cid)
        if re.fullmatch(currency.validate, number):
            with transaction.atomic():
                w, _ = Wallet.objects.get_or_create(user=user, currency=currency)
                w.number = number
                w.save()
                keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(ButtonText(user.lang).wallet, callback_data=ContextData.WALLET)
                    ],
                    [
                        InlineKeyboardButton(ButtonText(user.lang).back_home, callback_data=ContextData.HOME)
                    ]
                ])
                update.message.reply_html("✅ Kartani saqlandi",
                                          reply_markup=keyboard)
                return ALL
        else:
            update.message.reply_html(f"<pre>{currency.example}</pre>\nquyidagicha kiriting")


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
                text=ButtonText(user.lang).get_changes_for_excel_button, callback_data='none'
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
