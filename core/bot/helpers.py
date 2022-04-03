from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from account.models import BotUser


class Message:
    def __init__(self, lang):
        if lang == "uz":
            self.HOME = "🤓Valyuta ayirboshlash xizmatiga xush kelibsiz. Siz bilan ko‘rishib turganimizdan xursandmiz." \
                        "\n\n☝️Eslatma: Siz bizning botimiz orqali o‘z pullaringizni boshqa " \
                        "valyutalar bilan tezkor ayirboshlashingiz  mumkin!"
            self.settings = "⚙️ Sozlamalar"
            self.feedback = """👨‍💻 @Uzchangenetbot - Самая надежная и удобная система обмена электронных валют в Узбекистане!!!

⁉ Если у вас есть какие - либо вопросы или предложения относительно наших услуг, пожалуйста, свяжитесь с нами. 

💹 @uzchange_pay

Центр поддержки: 👨‍💻 @ikromjon_xusanov

💸Все транзакции: 68868
👥Все пользователи: 43721

👨‍💻Разработчик: @ikromjon_xusanov
"""
            self.set_full_name = "To'liq ismingizni kiriting"
        else:
            self.HOME = "🤓Добро пожаловать в пункт обмена валюты. Приятно познакомиться." \
                        "\n \n☝️Примечание: Вы можете перевести свои деньги через нашего бота" \
                        "Вы можете быстро обменять валюту!"
            self.settings = "⚙️ Настройки"
            self.feedback = """👨‍💻 @Uzchangenetbot - Самая надежная и удобная система обмена электронных валют в Узбекистане!!!

⁉ Если у вас есть какие - либо вопросы или предложения относительно наших услуг, пожалуйста, свяжитесь с нами. 

💹 @uzchange_pay

Центр поддержки: 👨‍💻 @ikromjon_xusanov

💸Все транзакции: 68868
👥Все пользователи: 43721

👨‍💻Разработчик: @ikromjon_xusanov
"""
            self.set_full_name = "Введите ваше полное имя"


class ButtonText:
    def __init__(self, lang):
        if lang == "uz":
            self.currency_exchange = "♻️ Valyuta ayirboshlash"
            self.wallet = "🔰 Hamyonlar"
            self.course_reserve = "📈 Kurs / 💰 Zahira"
            self.exchanges = "🧾 Almashuvlar"
            self.feedback = "📞 Qayta aloqa"
            self.settings = "⚙️ Sozlamalar"
            self.set_lang = "📝 Tilni o'zgartirish"
            self.set_full_name = "✏ F.I.SH o'zgartirish"
            self.back = "🔙 Orqaga"
        else:
            self.currency_exchange = "♻️ Обмен валюты"
            self.wallet = "🔰 Кошельки"
            self.course_reserve = "📈 Курс / 💰 Забронировать"
            self.exchanges = "🧾 Обмены"
            self.feedback = "📞 Обратная связь"
            self.settings = "⚙️ Настройки"
            self.set_lang = "📝 Изменить язык"
            self.set_full_name = "✏ Изменение Ф.И.О."
            self.back = "🔙 Назад"


class ContextData:
    HOME = "home"
    SETTINGS = "settings"
    FEEDBACK = 'feedback'


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
            InlineKeyboardButton(ButtonText(lang).feedback, callback_data=ContextData.FEEDBACK)
        ],
    ])


def get_bot_user(tg_id=None):
    return BotUser.objects.get_or_create(tg_id=tg_id)[0]
