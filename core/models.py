import os
from django.db import models

from account.models import BotUser


class Currency(models.Model):
    name = models.CharField("Nomi", max_length=100, null=True)
    buy = models.FloatField("Sotib olish", null=True, blank=True)
    sell = models.FloatField("Sotish", null=True, blank=True)
    validate = models.CharField("Validatsiya", max_length=100, null=True, blank=True)
    code = models.CharField("Kod", max_length=6)
    reserve = models.FloatField("Zaxira")
    example = models.CharField("Misol uchun", max_length=50)
    flag = models.CharField("Bayroq", max_length=5, default="🏳")
    is_sell = models.BooleanField("Sotiladimi?", default=True)
    is_buy = models.BooleanField("Sotib olinadimi?", default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "Valyuta"
        verbose_name_plural = "Valyutalar"


class CurrencyMinBuy(models.Model):
    from_card = models.ForeignKey(Currency, verbose_name="Valyutadan", on_delete=models.CASCADE,
                                  related_name='from_card')
    to_card = models.ForeignKey(Currency, verbose_name="Valyutaga", on_delete=models.CASCADE, related_name='to_card')
    min_buy_f = models.FloatField("Minimum valyutadan", null=True)
    min_buy_t = models.FloatField("Minimum valyutaga", null=True)

    def save(self, *args, **kwargs):
        c = CurrencyMinBuy.objects.filter(from_card=self.from_card, to_card=self.to_card).first()
        if not c or c.id == self.id:
            super(CurrencyMinBuy, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Valyutani minimum sotish"
        verbose_name_plural = verbose_name


class AcceptableCurrency(models.Model):
    currency = models.ForeignKey(Currency, verbose_name="Valyuta", on_delete=models.CASCADE, related_name='currency')
    acceptable = models.ManyToManyField(Currency, verbose_name="Ayirboshlash mumkin bo'lgan valyutalar",
                                        related_name='acceptable_currency', blank=True)

    def __str__(self):
        return self.currency.name

    class Meta:
        verbose_name = "Mos Valyuta"
        verbose_name_plural = "Mos Valyutalar"


class Wallet(models.Model):
    user = models.ForeignKey(BotUser, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, verbose_name="Valyuta turi", on_delete=models.CASCADE)
    number = models.CharField(max_length=50, verbose_name="Nomeri")

    def __str__(self):
        return self.currency.name

    class Meta:
        verbose_name = "Hamyon"
        verbose_name_plural = "Hamyonlar"


class Exchange(models.Model):
    STATUS = (
        ('Tekshiruvda', 'Tekshiruvda'),
        ('Bekor qilingan', "Bekor qilingan"),
        ("Muvaffaqiyatli tugadi", "Muvaffaqiyatli tugadi")
    )
    user = models.ForeignKey(BotUser, verbose_name="Foydalanuvchi", on_delete=models.SET_NULL, null=True)
    from_card = models.ForeignKey(Currency, verbose_name="Valyutadan", on_delete=models.SET_NULL, null=True,
                                  related_name='from_card_name')
    to_card = models.ForeignKey(Currency, verbose_name="Valyutaga", on_delete=models.SET_NULL, null=True,
                                related_name='to_card_name')
    from_number = models.CharField(max_length=50, verbose_name="Nomerdan", null=True)
    to_number = models.CharField(max_length=50, verbose_name="Nomerga", null=True)
    give = models.FloatField(default=0, verbose_name="Berish")
    give_code = models.CharField(max_length=10, null=True, verbose_name="Berish kodi")
    get = models.FloatField(default=0, verbose_name="Olish")
    get_code = models.CharField(max_length=10, null=True, verbose_name="Olish kodi")
    status = models.CharField(choices=STATUS, default='being check', max_length=60)

    class Meta:
        verbose_name = "Ayirboshlash"
        verbose_name_plural = "Ayirboshlashlar"


class Excel(models.Model):
    name = models.CharField("Nomi", max_length=50, null=True)
    from_user = models.ForeignKey(BotUser, verbose_name='Kim tomonidan ko\'rilgan', on_delete=models.SET_NULL,
                                  null=True)
    file = models.FileField("Fayl", default='static/null.xlsx')
    create_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.system(f"rm -rf uploads/{self.file.name}")
        super(Excel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Ma'lumot"
        verbose_name_plural = "Ma'lumotlar"


class OwnerCardNumber(models.Model):
    currency = models.ForeignKey(Currency, verbose_name="Valyuta turi", on_delete=models.CASCADE)
    number = models.CharField(max_length=50, verbose_name="Nomeri")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Admin kartalari"
        verbose_name_plural = verbose_name
