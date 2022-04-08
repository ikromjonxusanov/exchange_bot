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
    min_buy = models.FloatField(null=True)
    flag = models.CharField(max_length=5, default="🏳")
    is_sell = models.BooleanField(default=True)
    is_buy = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AcceptableCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    acceptable = models.ManyToManyField(Currency, related_name='acceptable_currency', blank=True)

    def __str__(self):
        return self.currency.name


class Wallet(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)


class Exchange(models.Model):
    from_card = models.CharField(max_length=50)
    to_card = models.CharField(max_length=50)
    summa = models.DecimalField(max_digits=12, decimal_places=6)
