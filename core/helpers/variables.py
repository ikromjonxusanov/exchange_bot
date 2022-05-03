from datetime import datetime
from telegram.ext import CallbackContext

from account.models import BotUser
from core.models import Exchange, Currency, Wallet, CurrencyMinBuy


def get_feedback(lang):
    if lang == 'uz':
        return (
            "Bot 08:00 dan 00:00 gacha kun davomida ruchnoy rejimda ishlaydi, operator tomonidan 5 daqiqadan 10 daqiqagacha bajariladi.\n\n"
            "🔗Bizning blogimiz linki:\n"
            "@change_bot_test_chat\n\n"
            "💁‍♂️Agar bizning xizmatimizga tegishli har qanday savol / takliflaringiz bo'lsa, bemalol murojat qilishingiz mumkin.\n"
            "🕙Texnik yordam ish vaqti soatlari:\n"
            "08:00 dan 00:00 gacha\n\n"
            "👨‍💻Qo'llab-quvvatlash: @ikromjonxusanov"
        )
    else:
        return (
            "Бот работает в ручном режиме с 08:00 до 00:00 в течение дня, выполняется оператором от 5 до 10 минут.\n\n"
            "🔗Ссылка на наш блог:\n"
            "@change_bot_test_chat\n\n"
            "💁‍♂️Если у вас есть какие-либо вопросы/предложения относительно нашего сервиса, не стесняйтесь обращаться к нам.\n"
            "🕙Часы работы технической поддержки:\n"
            "с 08:00 до 00:00\n\n"
            "👨‍💻Поддержка: @ikromjonxusanov"
        )


class Message:
    def __init__(self, lang):
        self.lang = lang
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

    @property
    def get_data_excel_error(self):
        if self.lang == 'uz':
            return "🤖 Ma'lumotni olishda xatolik yuz berdi ❌"
        else:
            return "🤖 Произошла ошибка при получении данных ❌"

    @property
    def data_excel(self):
        return "✏ Botda to'plangan ma'lumotlar" if self.lang == 'uz' else "✏ Данные, собранные в боте"


def wallet_add_or_change(create: bool, lang: str) -> str:
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


class ButtonText:
    def __init__(self, lang):
        self.lang = lang
        if lang == "uz":
            self.currency_exchange = "♻️ Valyuta ayirboshlash"
            self.wallet = "🔰 Hamyonlar"
            self.course_reserve = "📈 Kurs / 💰 Zahira"
            self.exchanges_history = "🧾 Almashuvlar"
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
            self.data = "📔 Ma'lumotlarni yuklab olish"
            self.give = "⬆️Berishni kiritish "
            self.get = "⬇️Olish kiritish "
            self.refferal = "👥 Referal"
        else:
            self.currency_exchange = "♻️ Обмен валюты"
            self.wallet = "🔰 Кошельки"
            self.course_reserve = "📈 Курс / 💰 Забронировать"
            self.exchanges_history = "🧾 Обмены"
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
            self.data = "📔 Скачать данные"
            self.give = "⬆ Отдать "
            self.get = "⬇ Получить "
            self.refferal = "👥 Реферал"

    @property
    def get_users_for_excel_button(self) -> str:
        return "📈 Foydalanuvchilar ma'lumotlari" if self.lang == 'uz' else "📈 информация о пользователе"

    @property
    def get_changes_for_excel_button(self) -> str:
        return "💱 O'tkazmalar ma'lumotlari" if self.lang == 'uz' else "💱 Информация о переносе"

    @property
    def exchange_create(self):
        return "💸 To'lovga o'tish" if self.lang == 'uz' else "💸 Перейти к оплате"

    @property
    def exchange_save(self):
        return "✅ O'tkazdim" if self.lang == 'uz' else "✅ Проводится"


def exchange_create_message(lang: str, owner_card_number: str, e: dict) -> str:
    if lang == 'uz':
        return f"<pre>{owner_card_number}</pre>\n👆\n" \
               f"Almashuvingiz muvaffaqiyatli bajarilishi uchun quyidagi harakatlarni amalga oshiring:" \
               f"Pastroqda ko‘rsatilgan miqdorni <pre>{owner_card_number}</pre>" \
               "hamyon raqamiga o‘tkazing; <b>«O‘tkazdim»</b> tugmasini bosing; \nMiqdor: " \
               f"<b>{e['give']}</b> {e['give_code']}" \
               "Ushbu tekshiruv operator tomonidan amalga oshiriladi va o‘rtacha 5 daqiqadan 60 daqiqagacha davom etadi"
    else:
        return f"<pre>{owner_card_number}</pre>\n👆\n" \
               f"Для успешной обработки вашей заявки пожалуйста выполните следующие действия:" \
               f"Переведите указанную ниже сумму на кошелек <pre>{owner_card_number}</pre>" \
               "Нажмите на кнопку «Проводится»; \nMiqdor: " \
               f"<b>{e['give']}</b> {e['give_code']}" \
               "Данная операция производится оператором в ручном режиме и занимает в среднем" \
               " от от 5 минуты до 60 минут в рабочее время"


class ContextData:
    HOME = "home"
    SETTINGS = "settings"
    FEEDBACK = 'feedback'
    EXCHANGE = 'exchange'
    RESERVE = 'reserve'
    WALLET = "wallet"


ContextData = ContextData()


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


def get_exchange_text(lang: str, from_card: Currency, to_card: Currency) -> str:
    if lang == 'uz':
        return "⬆️<b>Berish</b>: <i>{}</i>\n⬇️<b>Olish</b>: <i>{}</i>\n🕗<b>Sana</b>: {:%d.%m.%Y}".format(
            from_card.name,
            to_card.name,
            datetime.now()
        )
    else:
        return "⬆️<b>Отдаете</b>: <i>{}</i>\n⬇️<b>Получаете</b>: <i>{}</i>\n🕗<b>Дата создания</b>: {:%d.%m.%Y}".format(
            from_card.name,
            to_card.name,
            datetime.now()
        )


def exchange_from_card_msg(from_card, minbuy: CurrencyMinBuy, code: str, lang: str) -> str:
    if lang == 'uz':
        return f"⬆ ️Berish miqdorini <b>{from_card.name}</b>da kiriting:\n\n" \
               f"Minimal:  <i>{minbuy.min_buy_f}</i> {code}\n" \
               "Bekor qilish uchun /start deb yozing."
    else:
        return f"⬆️Введите сумму отдачи в <b> {from_card.name} </b>: \n\n" \
               f"Минимум: <i> {minbuy.min_buy_f} </i> {code}\n" \
               "Для отмены напишите /start"


def exchange_to_card_msg(to_card: Currency, minbuy: CurrencyMinBuy, code: str, lang: str) -> str:
    if lang == 'uz':
        return f"⬇ Olish miqdorini <b>{to_card.name}</b>da kiriting:\n\n" \
               f"Minimal:  <i>{minbuy.min_buy_t}</i> {code}\n" \
               "Bekor qilish uchun /start deb yozing."
    else:
        return f"⬇ Введите сумму получения в <b> {to_card.name} </b>: \n\n" \
               f"Минимум: <i> {minbuy.min_buy_t} </i> {code}\n" \
               "Для отмены напишите /start"


def enter_card_number_msg(card: Currency, lang: str) -> str:
    if lang == "uz":
        return "<i>Siz to‘lov qilmoqchi bo‘lgan</i>" \
               f"\n\n<b>{card.name}</b> raqamni kiriting:" \
               f"\nMisol uchun: (<i>{card.example}</i>)"
    else:
        return f"Введите номер <b>{card.name}</b> счёта:" \
               "\nС которого хотите совершить оплату." \
               f"\nНапример: (<i>{card.example}</i>)"


def enter_repeat_card_number_msg(card: Currency, lang: str) -> str:
    if lang == "uz":
        return f"{card.name} hamyon formati noto'g'ri"
    else:
        return f"Неверный формат {card.name} кошелька"


def enter_min_summa_msg(minbuy_value: float, code: str, lang: str) -> str:
    if lang == "uz":
        return f"Minimal:  <i>{minbuy_value}</i> {code}\n" \
               "Bekor qilish uchun /start deb yozing."
    else:
        return f"Минимум: <i> {minbuy_value} </i> {code}\n" \
               "Для отмены напишите /start"


def get_card_code(card: Currency, lang: str) -> str:
    code = card.code
    if card.code == 'UZS':
        code = 'So`m'
        if lang == 'ru':
            code = "СУМ"
    return code


def get_status(status: str, lang: str):
    if lang == 'uz':
        if status == 'checking':
            return "Tekshiruvda"
        elif status == "cancel":
            return "Admin tomonidan bekor qilingan"
        elif status == "success":
            return "Muvaffaqiyatli tugadi"
    else:
        if status == 'checking':
            return "В обработке"
        elif status == "cancel":
            return "Админ отменил сделку"
        elif status == "success":
            return "Успешно завершено"


def get_exchange_doc_msg(exchange: Exchange, lang: str) -> str:
    date = "{:%d.%m.%Y %H:%M}".format(datetime.now())
    status = get_status(exchange.status, lang)
    if lang == "uz":
        return (f"🆔 Almashuv: {exchange.id}"
                f"<br/>🔀:{exchange.from_card} ➡️ {exchange.to_card}"
                f"<br/>{exchange.from_card.flag}{exchange.from_card}: {exchange.from_number}"
                f"<br/>💸: {exchange.give} {exchange.give_code}"
                f"<br/>{exchange.to_card.flag}{exchange.to_card}: {exchange.to_number}"
                f"<br/>💰: {exchange.get} {exchange.get_code}"
                f"<br/>📌To‘lov: {status}."
                f"<br/>📆O‘tkazma sanasi: {date}"
                )
    else:
        return (f"🆔 Заявка: {exchange.id}"
                f"\n🔀:{exchange.from_card} ➡️ {exchange.to_card}"
                f"\n{exchange.from_card.flag}{exchange.from_card}: {exchange.from_number}"
                f"\n💸: {exchange.give} {exchange.give_code}"
                f"\n{exchange.to_card.flag}{exchange.to_card}: {exchange.to_number}"
                f"\n💰: {exchange.get} {exchange.get_code}"
                f"\n📌 Статус оплаты: {status}."
                f"\n📆Дата заявки: {date}"
                )


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


def referral_msg(user: BotUser, context: CallbackContext):
    if user.lang == "uz":
        return (
            "👥 <b>Referal</b>"
            "\n💰 <b>Balansingiz</b>: <i>0</i> so'm"
            "\n<i>Do'stlaringizni botga taklif qiling va ro'yxatdan o'tgan 50 so'm sizning hisobingizga tushadi</i>"
            f"\n<b>Sizning havolangiz</b>: t.me/{context.bot.username}?start={user.tg_id}"
        )
    else:
        return (
            "👥 Реферал"
            "\n💰 <b>Ваш баланс</b>: <i>0</i> сум"
            "\n<i>Пригласите своих друзей в бота и зарегистрированные 50 сумов будут зачислены на ваш счет</i>"
            f"\n <b> Ваша ссылка </b>: t.me/{context.bot.username}?start={user.tg_id}"
        )


def referral_button_text(lang):
    if lang == 'uz':
        return {
            "read-more": "📑 Batafsil",
            "withdraw-money": "📥 Pul yechish",
            "my-referrals": "👥 Referallarim",
        }
    else:
        return {
            "read-more": "📑 Прочитайте больше",
            "withdraw-money": "📥 Снять деньги",
            "my-referrals": "👥 Мои рефералы",
        }


def referral_read_me(lang):
    if lang == 'uz':
        return "Do'stlaringizni botga taklif qiling va ro'yxatdan o'tgan 50 so'm sizning hisobingizga tushadi"
    else:
        return "Пригласите своих друзей в бота и зарегистрированные 50 сумов будут зачислены на ваш счет"


def my_referrals_msg(lang, count):
    if lang == 'uz':
        return f"Foydalanuvchilar soni {count} ta"
    else:
        return f"Количество пользователей {count}"


def withdraw_money_msg(lang):
    if lang == 'uz':
        return "Yechish uchun eng kam mablag' miqdori 100 000 UZS"
    else:
        return "Минимальная сумма для решения 100 000 сум"
