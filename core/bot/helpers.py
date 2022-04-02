from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from account.models import BotUser


class Message:
    def __init__(self, lang):
        if lang == "uz":
            self.HOME = "🤓Valyuta ayirboshlash xizmatiga xush kelibsiz. Siz bilan ko‘rishib turganimizdan xursandmiz." \
                        "\n\n☝️Eslatma: Siz bizning botimiz orqali o‘z pullaringizni boshqa " \
                        "valyutalar bilan tezkor ayirboshlashingiz  mumkin!"
            self.settings = "⚙️ Sozlamalar"
        else:
            self.HOME = "🤓Добро пожаловать в пункт обмена валюты. Приятно познакомиться." \
                        "\n \n☝️Примечание: Вы можете перевести свои деньги через нашего бота" \
                        "Вы можете быстро обменять валюту!"
            self.settings = "⚙️ Настройки"


class ButtonText:
    def __init__(self, lang):
        if lang == "uz":
            self.currency_exchange = "♻️ Valyuta ayirboshlash"
            self.wallet = "🔰 Hamyonlar"
            self.course_reserve = "📈 Kurs / 💰 Zahira"
            self.exchanges = "🧾 Almashuvlar"
            self.contact = "📞 Qayta aloqa"
            self.settings = "⚙️ Sozlamalar"
        else:
            self.currency_exchange = "♻️ Обмен валюты"
            self.wallet = "🔰 Кошельки"
            self.course_reserve = "📈 Курс / 💰 Забронировать"
            self.exchanges = "🧾 Обмены"
            self.contact = "📞 Обратная связь"
            self.settings = "⚙️ Настройки"


class ContextData:
    HOME = "home"
    SETTINGS = "settings"


ContextData = ContextData()


def get_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(ButtonText(lang).currency_exchange, callback_data=ContextData.HOME),
            InlineKeyboardButton(ButtonText(lang).wallet, callback_data=ContextData.HOME),
        ],
        [
            InlineKeyboardButton(ButtonText(lang).exchanges, callback_data=ContextData.HOME),
            InlineKeyboardButton(ButtonText(lang).course_reserve, callback_data=ContextData.HOME)
        ],
        [
            InlineKeyboardButton(ButtonText(lang).settings, callback_data=ContextData.SETTINGS),
            InlineKeyboardButton(ButtonText(lang).contact, callback_data=ContextData.HOME)
        ],
    ])


def get_bot_user(tg_id=None):
    return BotUser.objects.get_or_create(tg_id=tg_id)[0]
