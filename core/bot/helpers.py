from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from account.models import BotUser
from core.models import Exchange, Currency, Wallet


def get_feedback(lang):
    exchanges = Exchange.objects.count()
    clients = BotUser.objects.count()
    if lang == 'uz':
        return f"""👨‍💻 @Uzchangenetbot - Самая надежная и удобная система обмена электронных валют в Узбекистане!!!

⁉ Если у вас есть какие - либо вопросы или предложения относительно наших услуг, пожалуйста, свяжитесь с нами. 

💹 @uzchange_pay

Центр поддержки: 👨‍💻 @ikromjon_xusanov

💸Все транзакции: {exchanges}
👥Все пользователи: {clients}

👨‍💻Разработчик: @ikromjon_xusanov
        """
    else:
        return f"""👨‍💻 @Uzchangenetbot - Самая надежная и удобная система обмена электронных валют в Узбекистане!!!

        ⁉ Если у вас есть какие - либо вопросы или предложения относительно наших услуг, пожалуйста, свяжитесь с нами. 

        💹 @uzchange_pay

        Центр поддержки: 👨‍💻 @ikromjon_xusanov

        💸Все транзакции: {exchanges}
        👥Все пользователи: {clients}

        👨‍💻Разработчик: @ikromjon_xusanov
        """


class Message:
    def __init__(self, lang):
        if lang == "uz":
            self.HOME = "🤓Valyuta ayirboshlash xizmatiga xush kelibsiz. Siz bilan ko‘rishib turganimizdan xursandmiz." \
                        "\n\n☝️Eslatma: Siz bizning botimiz orqali o‘z pullaringizni boshqa " \
                        "valyutalar bilan tezkor ayirboshlashingiz  mumkin!"
            self.settings = "⚙️ Sozlamalar"
            self.set_full_name = "To'liq ismingizni kiriting"
            self.exchange = "Valyutalarni tanlang: (🔷Berish) va (🔶Olish)"
            self.reserve = "💰<b>Bot Zahirasi</b>"
            self.wallet = "🗂 Sizning hamyonlaringiz:"
        else:
            self.HOME = "🤓Добро пожаловать в пункт обмена валюты. Приятно познакомиться." \
                        "\n \n☝️Примечание: Вы можете перевести свои деньги через нашего бота" \
                        "Вы можете быстро обменять валюту!"
            self.settings = "⚙️ Настройки"
            self.set_full_name = "Введите ваше полное имя"
            self.exchange = "Выберите валюты для обмена: (🔷отдача) и (🔶получения)"
            self.reserve = "💰<b>Резерв Обменника</b>"
            self.wallet = "🗂 Ваши Кошельки:"

        self.feedback = get_feedback(lang)


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
            self.cancel = "❌ Bekor qilish"
            self.back = "🔙 Orqaga"
            self.back_home = "📤 Bosh menyu"
            self.reserve = "💰 Zahirani ko'rsatish"
            self.course = "📈 Kursni ko'rsatish"
            self.delete = "❌ Ma'lumotlarni o'chirish"
            self.delete_wallet = "❌ O'chirish"
            self.yes = "✅ Ha"
            self.no = "❌ Yo'q"
        else:
            self.currency_exchange = "♻️ Обмен валюты"
            self.wallet = "🔰 Кошельки"
            self.course_reserve = "📈 Курс / 💰 Забронировать"
            self.exchanges = "🧾 Обмены"
            self.feedback = "📞 Обратная связь"
            self.settings = "⚙️ Настройки"
            self.set_lang = "📝 Изменить язык"
            self.set_full_name = "✏ Изменение Ф.И.О."
            self.cancel = "❌ Отмена"
            self.back = "🔙 Назад"
            self.back_home = "📤 Главное меню"
            self.reserve = "💰 Показать Резервы"
            self.course = "📈 Показать Курс"
            self.delete = "❌ Удалить данные"
            self.delete_wallet = "❌ Удалить"
            self.yes = "✅ Да"
            self.no = "❌ Нет"

    def wallet_add_or_change(self, create: bool, lang: str) -> str:
        if lang == 'uz':
            if create:
                return "➕ Qo'shish"
            else:
                return "✏ O'zgartirish"
        else:
            if create:
                return "➕ Добавлять"
            else:
                return "✏ Изменить"


class ContextData:
    HOME = "home"
    SETTINGS = "settings"
    FEEDBACK = 'feedback'
    EXCHANGE = 'exchange'
    RESERVE = 'reserve'
    WALLET = "wallet"


ContextData = ContextData()


def get_keyboard(lang):
    return InlineKeyboardMarkup([
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
    ])


def get_bot_user(tg_id=None):
    return BotUser.objects.get_or_create(tg_id=tg_id)[0]


def get_text_wallet(user: BotUser):
    currencies = list(Currency.objects.all().values('id', 'name'))
    txt = "\n"
    for c in currencies:
        card = Wallet.objects.filter(user=user, currency_id=c['id']).first()
        resp = card.number if card else "Bo'sh" if user.lang == 'uz' else "Пустой"
        txt += f"\n💳 <b>{c['name']}</b>: <i>{resp}</i>"
    return txt
