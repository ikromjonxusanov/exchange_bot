import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from core.decorators import login_user_query, login_user
from core.handlers.core import home
from core.helpers.keyboards import exchange_retrieve_keyboard, exchange_get_keyboard, \
    exchange_give_keyboard, currencies_keyboard
from core.helpers.variables import get_bot_user, Message, ButtonText, get_exchange_text, get_card_code, \
    exchange_from_card_msg, exchange_to_card_msg, enter_card_number_msg, enter_min_summa_msg, \
    enter_repeat_card_number_msg, exchange_create_message, get_exchange_doc_msg
from core.models import Currency, CurrencyMinBuy, Wallet, OwnerCardNumber, Exchange
from core.states import ENTER_SUMMA, ADD_FROM_CARD, ADD_TO_CARD, ALL


@login_user_query
def currency_exchange(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(
        text=Message(user.lang).exchange,
        parse_mode="HTML",
        reply_markup=currencies_keyboard(user.lang)
    )


@login_user_query
def give(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    pk = int(query.data.split('/')[1])
    currency = Currency.objects.get(id=pk)
    try:
        query.edit_message_text(
            text=Message(user.lang).exchange,
            parse_mode="HTML",
            reply_markup=exchange_give_keyboard(user.lang, currency)
        )
    except BadRequest:
        pass


@login_user_query
def get(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    pk = int(query.data.split('/')[1])
    query.answer()
    currency = Currency.objects.get(id=pk)
    try:
        query.edit_message_text(
            text=Message(user.lang).exchange,
            parse_mode="HTML",
            reply_markup=exchange_get_keyboard(user.lang, currency)
        )
    except BadRequest:
        pass


@login_user_query
def exchange_retrieve(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    from_card = Currency.objects.filter(id=int(query.data.split('/')[1])).first()
    to_card = Currency.objects.filter(id=int(query.data.split('/')[2])).first()
    keyboard = exchange_retrieve_keyboard(user.lang, from_card.name, to_card.name)
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
    user = get_bot_user(query.from_user.id)
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    if minbuy:
        code = get_card_code(from_card, user.lang)

        msg = exchange_from_card_msg(from_card, minbuy, code, user.lang)
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
    user = get_bot_user(query.from_user.id)
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    if minbuy:
        code = get_card_code(to_card, user.lang)
        msg = exchange_to_card_msg(to_card, minbuy, code, user.lang)
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
    user = get_bot_user(update.effective_user.id)
    code = get_card_code(card, user.lang)

    try:
        if minbuy.to_card == context.user_data['code']:
            minbuy_value = minbuy.min_buy_t
            code = get_card_code(to_card, user.lang)
        summa = float(update.message.text)
        if minbuy_value <= summa:
            keyboard = ReplyKeyboardMarkup([])
            wallet_user = Wallet.objects.filter(user=user, currency=from_card).first()
            if wallet_user:
                keyboard = ReplyKeyboardMarkup([
                    [wallet_user.number]
                ], one_time_keyboard=True, resize_keyboard=True)
            msg = enter_card_number_msg(from_card, user.lang)
            update.message.reply_html(
                msg,
                reply_markup=keyboard)
            context.user_data['exchange'] = {'summa': summa}
            return ADD_FROM_CARD
        else:
            update.message.reply_html(
                enter_min_summa_msg(minbuy_value, code, user.lang)
            )
    except ValueError:
        update.message.reply_html(
            enter_min_summa_msg(minbuy_value, code, user.lang)
        )


@login_user
def enter_from_card(update: Update, context: CallbackContext):
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    try:
        validate = re.fullmatch(from_card.validate, update.message.text)
    except TypeError:
        validate = True
    if validate:
        user = get_bot_user(update.effective_user.id)
        wallet_number = Wallet.objects.filter(user=user, currency=to_card).first()
        keyboard = ReplyKeyboardMarkup([])
        if wallet_number:
            keyboard = ReplyKeyboardMarkup([
                [wallet_number.number]
            ], one_time_keyboard=True, resize_keyboard=True)
        msg = enter_card_number_msg(to_card, user.lang)
        update.message.reply_html(msg,
                                  reply_markup=keyboard)
        context.user_data['exchange']['from_card'] = update.message.text
        return ADD_TO_CARD
    else:
        user = get_bot_user(update.effective_user.id)
        wallet_number = Wallet.objects.filter(user=user, currency=from_card).first()
        keyboard = ReplyKeyboardMarkup([])
        if wallet_number:
            keyboard = ReplyKeyboardMarkup([
                [wallet_number.number]
            ], one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_html(
            enter_repeat_card_number_msg(from_card, user.lang),
            reply_markup=keyboard)


@login_user
def enter_to_card(update: Update, context: CallbackContext):
    user = get_bot_user(update.message.from_user.id)
    from_card = context.user_data['from_card']
    to_card = context.user_data['to_card']
    summa = context.user_data['exchange']['summa']
    minbuy = CurrencyMinBuy.objects.filter(from_card=from_card, to_card=to_card).first()
    try:
        validate = re.fullmatch(to_card.validate, update.message.text)
    except TypeError:
        validate = True
    if validate:
        give_price = None
        get_price = None
        give_code = get_card_code(from_card, user.lang)
        get_code = get_card_code(to_card, user.lang)
        if str(from_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == from_card:
            get_price = "%.2f" % (float(summa) / to_card.sell)
            give_price = "%.2f" % float(summa)
        elif str(from_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == to_card:
            get_price = "%.2f" % float(summa)
            give_price = "%.2f" % (float(summa) * to_card.sell)
        elif str(to_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == from_card:
            get_price = "%.2f" % (float(summa) * from_card.buy)
            give_price = "%.2f" % float(summa)
        elif str(to_card.code).lower() in ("uz", "uzs") and context.user_data['code'] == to_card:
            get_price = "%.2f" % float(summa)
            give_price = "%.2f" % (float(summa) / from_card.buy)
        elif context.user_data['code'] == from_card:
            get_price = "%.2f" % (float(summa) * (minbuy.min_buy_t / minbuy.min_buy_f))
            give_price = "%.2f" % float(summa)
        elif context.user_data['code'] == to_card:
            get_price = "%.2f" % float(summa)
            give_price = "%.2f" % (minbuy.min_buy_t / minbuy.min_buy_f * float(summa))
        context.user_data['e'] = {
            "user": user,
            "from_card": from_card,
            "to_card": to_card,
            "from_number": context.user_data['exchange']['from_card'],
            "to_number": update.message.text,
            "give": give_price,
            "give_code": give_code,
            "get": get_price,
            "get_code": get_code
        }
        msg = "🔖Sizning almashuv:" if user.lang == 'uz' else "🔖Ваша заявка"
        update.message.reply_html(
            f"{msg}\n\n🔀:{from_card} ➡️ {to_card}"
            f"\n⬆ {give_price} {give_code}"
            f"\n⬇ {get_price} {get_code}"
            f"\n{from_card.flag} {from_card.name}: {context.user_data['exchange']['from_card']}"
            f"\n{to_card.flag} {to_card.name}: {update.message.text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text=ButtonText(user.lang).exchange_create,
                                      callback_data="exchange_create")],
                [InlineKeyboardButton(text=ButtonText(user.lang).cancel, callback_data="home")]
            ])
        )
        return ALL
    else:
        wallet_number = Wallet.objects.filter(user=user, currency=to_card).first()
        keyboard = ReplyKeyboardMarkup([])
        if wallet_number:
            keyboard = ReplyKeyboardMarkup([
                [wallet_number.number]
            ], one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_html(
            enter_repeat_card_number_msg(to_card, user.lang),
            reply_markup=keyboard)


@login_user_query
def exchange_create(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    try:
        e = context.user_data['e']
        owner_card_number = OwnerCardNumber.objects.order_by('?').filter(
            currency=context.user_data['from_card']).first()
        query.edit_message_text(
            text=exchange_create_message(user.lang, owner_card_number, e),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text=ButtonText(user.lang).exchange_save, callback_data="exchange_save")],
                [InlineKeyboardButton(text=ButtonText(user.lang).cancel, callback_data="home")]
            ])
        )
    except KeyError:
        query.answer(show_alert=True, text="⌛ Vaqtingiz o'tib ketdi" if user.lang == 'uz' else "⌛ Ваше время вышло")
        home(update, context)


@login_user_query
def exchange_save(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    exchange = Exchange.objects.create(**context.user_data['e'])
    msg = get_exchange_doc_msg(exchange, user.lang)
    query.edit_message_text("⏳")
    query.message.reply_html(
        msg
    )
    private = f"👤 {user.full_name}\n📞 {user.phone}\n"
    context.bot.send_message(chat_id="@change_bot_test_chat", parse_mode="html", text=msg)
    context.bot.send_message(chat_id="-779642309", parse_mode="html", text=private + msg)
    home(update, context, delete=False)
