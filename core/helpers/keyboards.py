from core.helpers.variables import ButtonText, ContextData
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from core.models import Currency, AcceptableCurrency


def exchange_cancel_back_buttons(lang):
    return [
        [InlineKeyboardButton(text=ButtonText(lang).cancel, callback_data=ContextData.EXCHANGE)],
        [InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME)]
    ]


def get_keyboard(lang, admin: bool = False):
    buttons = [
        [
            InlineKeyboardButton(ButtonText(lang).currency_exchange, callback_data=ContextData.EXCHANGE),
            InlineKeyboardButton(ButtonText(lang).wallet, callback_data=ContextData.WALLET),
        ],
        [
            InlineKeyboardButton(ButtonText(lang).exchanges, callback_data='none'),
            InlineKeyboardButton(ButtonText(lang).course_reserve, callback_data='course_reserve')
        ],
        [
            InlineKeyboardButton(ButtonText(lang).settings, callback_data=ContextData.SETTINGS),
            InlineKeyboardButton(ButtonText(lang).feedback, callback_data=ContextData.FEEDBACK)
        ],
    ]
    if admin:
        buttons.append([InlineKeyboardButton(ButtonText(lang).data, callback_data='data')])
    return InlineKeyboardMarkup(buttons)


def reserve_keyboard(lang: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=ButtonText(lang).course, callback_data='course_reserve')
        ],
        [
            InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME),
        ]
    ])


def course_reserve_keyboard(lang: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=ButtonText(lang).reserve, callback_data=ContextData.RESERVE)
        ],
        [
            InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME),
        ]
    ])


def back_keyboard(lang):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME),
    ]])


def setting_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=ButtonText(lang).set_lang,
                callback_data='setLang'
            ),
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(lang).set_full_name,
                callback_data='setFullName'
            ),
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(lang).back,
                callback_data=ContextData.HOME
            ),
        ]
    ])


def admin_data(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=ButtonText(lang).get_users_for_excel_button, callback_data='users_excel'
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(lang).get_changes_for_excel_button, callback_data='exchanges_excel'
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText(lang).back_home, callback_data=ContextData.HOME
            )
        ]
    ])


def error_keyboard(lang):
    InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="👨🏻‍💻 Dasturchiga murojaat qilish" if lang == 'uz' else "👨🏻‍💻 Связаться с разработчиком",
                url="https://t.me/ikromjonxusanov"),
        ],
        [
            InlineKeyboardButton(text=ButtonText(lang).back_home, callback_data=ContextData.HOME)
        ]
    ])


def uz_ru_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data='uz'),
            InlineKeyboardButton(text="🇷🇺 русский язык", callback_data="ru")
        ]
    ])


def contact_keyboard(btn_text):
    return ReplyKeyboardMarkup([[KeyboardButton(btn_text, request_contact=True)]],
                               resize_keyboard=True, selective=True)


def exchange_retrieve_keyboard(lang, from_name, to_name):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=ButtonText(lang).give + from_name, callback_data="exchange_from_card")],
        [InlineKeyboardButton(text=ButtonText(lang).get + to_name, callback_data="exchange_to_card")],
        [InlineKeyboardButton(text=ButtonText(lang).cancel, callback_data=ContextData.HOME)],
    ])


def exchange_get_keyboard(lang: str, currency: Currency):
    keyboard = []
    currencies = Currency.objects.all()
    acceptablecurrencies = AcceptableCurrency.objects.filter(currency=currency).first()
    acceptable = acceptablecurrencies.acceptable.all()
    for c in currencies:
        data = [
            InlineKeyboardButton(text="➖", callback_data=f'none'),
            InlineKeyboardButton(text="🔶" + c.name, callback_data=f'get/{c.id}'),
        ]
        if c.id == currency.id:
            data[1] = InlineKeyboardButton(text="✅" + c.name, callback_data=f'get/{c.id}')
        keyboard.append(data)
    for i in range(len(acceptable)):
        keyboard[i][0] = InlineKeyboardButton(text="🔷" + acceptable[i].name,
                                              callback_data=f'exchange-retrieve/{acceptable[i].id}/{currency.id}')
    keyboard.extend(
        exchange_cancel_back_buttons(lang)
    )
    return InlineKeyboardMarkup(keyboard)


def exchange_give_keyboard(lang: str, currency: Currency):
    keyboard = []
    currencies = Currency.objects.all()
    acceptablecurrencies = AcceptableCurrency.objects.filter(currency=currency).first()
    acceptable = acceptablecurrencies.acceptable.all()
    for c in currencies:
        data = [
            InlineKeyboardButton(text="🔷" + c.name, callback_data=f'give/{c.id}'),
            InlineKeyboardButton(text="➖", callback_data=f'none')
        ]
        if c.id == currency.id:
            data[0] = InlineKeyboardButton(text="✅" + c.name, callback_data=f'give/{c.id}')
        keyboard.append(data)
    for i in range(len(acceptable)):
        keyboard[i][1] = InlineKeyboardButton(text="🔶" + acceptable[i].name,
                                              callback_data=f'exchange-retrieve/{currency.id}/{acceptable[i].id}')

    keyboard.extend(
        exchange_cancel_back_buttons(lang)
    )

    return InlineKeyboardMarkup(keyboard)


def currencies_keyboard(lang):
    keyboard = []
    currencies = Currency.objects.all()
    for c in currencies:
        keyboard.append([
            InlineKeyboardButton(text="🔷" + c.name, callback_data=f'give/{c.id}'),
            InlineKeyboardButton(text="🔶" + c.name, callback_data=f'get/{c.id}')
        ])
    keyboard.append([InlineKeyboardButton(text=ButtonText(lang).back, callback_data=ContextData.HOME)])
    return InlineKeyboardMarkup(keyboard)


def wallet_add_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(ButtonText(lang).wallet, callback_data=ContextData.WALLET)
        ],
        [
            InlineKeyboardButton(ButtonText(lang).back_home, callback_data=ContextData.HOME)
        ]
    ])
