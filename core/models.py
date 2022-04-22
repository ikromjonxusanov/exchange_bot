import os
from django.db import models

from account.models import BotUser


class Currency(models.Model):
    name = models.CharField(max_length=100, null=True)
    buy = models.FloatField(null=True, blank=True)
    sell = models.FloatField(null=True, blank=True)
    validate = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=6)
    reserve = models.FloatField()
    example = models.CharField(max_length=50)
    flag = models.CharField(max_length=5, default="🏳")
    is_sell = models.BooleanField(default=True)
    is_buy = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class CurrencyMinBuy(models.Model):
    from_card = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_card')
    to_card = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_card')
    min_buy_f = models.FloatField(null=True)
    min_buy_t = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not CurrencyMinBuy.objects.filter(from_card=self.from_card, to_card=self.to_card).exists():
            super(CurrencyMinBuy, self).save(*args, **kwargs)


class AcceptableCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    acceptable = models.ManyToManyField(Currency, related_name='acceptable_currency', blank=True)

    def __str__(self):
        return self.currency.name


class Wallet(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.currency.name


class Exchange(models.Model):
    STATUS = (
        ('new', 'Yangi'),
        ('fail', "Bekor qilingan"),
        ("success", "Muvaffaqiyatli tugadi")
    )
    user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True)
    from_card = models.CharField(max_length=50, null=True)
    to_card = models.CharField(max_length=50, null=True)
    summa = models.FloatField(default=0)
    status = models.CharField(choices=STATUS, default='new', max_length=60)


class Excel(models.Model):
    name = models.CharField(max_length=50, null=True)
    from_user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True)
    file = models.FileField(default='static/null.xlsx')
    create_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.system(f"rm -rf uploads/{self.file.name}")
        super(Excel, self).delete(*args, **kwargs)
