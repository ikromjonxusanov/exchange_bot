from telegram import Update
from telegram.ext import CallbackContext

from core.helpers.telegraf import text_to_telegraph
from core.helpers.variables import get_bot_user, Message, get_course_reserve, get_reserve, \
    get_exchange_doc_msg
from core.decorators import login_user_query
from core.helpers.keyboards import get_keyboard, reserve_keyboard, course_reserve_keyboard, back_keyboard, \
    setting_keyboard
from core.models import Exchange
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
    keyboard = setting_keyboard(user.lang)
    query.edit_message_text(
        text=Message(user.lang).settings,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = back_keyboard(user.lang)
    query.edit_message_text(
        text=Message(user.lang).feedback,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def set_full_name(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(update.callback_query.from_user.id)
    keyboard = back_keyboard(user.lang)
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
    keyboard = course_reserve_keyboard(user.lang)
    query.edit_message_text(
        text=get_course_reserve(user.lang),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def reserve(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    keyboard = reserve_keyboard(user.lang)
    query.edit_message_text(
        text=get_reserve(user.lang),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@login_user_query
def exchanges_history(update: Update, context: CallbackContext):
    query = update.callback_query
    user = get_bot_user(query.from_user.id)
    exchanges = Exchange.objects.filter(user=user).order_by("-pk")
    title = "Almashinuv tarixi" if user.lang == 'uz' else "?????????????? ????????????"
    msg = "<h3>???? Alamshuvlar</h3><br/>" if user.lang == 'uz' else "<h3>???? ????????????</h3><br/>"
    if len(exchanges) > 0:
        for i in range(len(exchanges)):
            msg += get_exchange_doc_msg(exchanges[i], user.lang)
            if i != len(exchanges)-1:
                msg += f"<br/>{'-'*75}<br/>"
    else:
        msg += "<i>Almashinuv tarixi topilmadi</i>" if user.lang == "uz" else "<i>?????????????? ?????????? ???? ????????????</i>"
    text = text_to_telegraph(title, msg)
    query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=back_keyboard(user.lang)
    )
