from core.bot.helpers import ButtonText, ContextData, Message
from core.models import Currency
from telegram import InlineKeyboardButton


def get_course_reserve(lang):
    if lang == 'ru':
        buy = "📉 <b>Курс Продажи</b>"
        sell = "📈 <b>Курс Покупки</b>"
        code = "СУМ"
    else:
        buy = "📉 <b>Sotish kursi</b>"
        sell = "📈 <b>Sotib olish kursi</b>"
        code = "so'm"

    data = f"{buy}"
    buy_currencies = Currency.objects.all().filter(is_buy=True)
    sell_currencies = Currency.objects.all().filter(is_sell=True)
    for b in buy_currencies:
        data += f"\n1 {b.name} = <b>{b.buy}</b> {code}"
    data += f"\n\n{sell}"
    for s in sell_currencies:
        data += f"\n1 {s.name} = <b>{s.sell}</b> {code}"
    return data


def get_reserve(lang):
    if lang == 'ru':
        code = "СУМ"
    else:
        code = "so'm"
    data = Message(lang).reserve + "\n"
    currencies = Currency.objects.all().values('name', "reserve", 'flag')
    for c in currencies:
        data += f"\n{c['flag']} {c['name']} = <b>{c['reserve']}</b> <b>{code}</b>"
    return data


def exchange_cancel_back_buttons(lang):
    return [
        [InlineKeyboardButton(text=ButtonText(lang).cancel, callback_data=ContextData.EXCHANGE)],
        [InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME)]
    ]
