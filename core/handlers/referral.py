from telegram import Update
from telegram.ext import CallbackContext

from core.helpers.variables import referral_msg, get_bot_user, referral_read_me, my_referrals_msg, withdraw_money_msg
from core.decorators import login_user_query
from core.helpers.keyboards import referral_keyboard, back_referral_keyboard


@login_user_query
def referral(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(
        referral_msg(user, context),
        parse_mode="HTML",
        reply_markup=referral_keyboard(user.lang),
    )


@login_user_query
def read_more(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.edit_message_text(
        text=referral_read_me(user.lang),
        parse_mode="HTML",
        reply_markup=back_referral_keyboard(user.lang)
    )


@login_user_query
def my_referrals(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    query.answer(my_referrals_msg(user.lang, 0))


@login_user_query
def withdraw_money(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    count = 0
    text = withdraw_money_msg(user.lang)
    if count >= 100000:
        query.edit_message_text(
            text=text
        )
    else:
        query.answer(show_alert=True, text="‼ "+text)
