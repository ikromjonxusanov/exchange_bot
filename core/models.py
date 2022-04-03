from django.db import models

from account.models import BotUser


class Currency(models.Model):
    name = models.CharField(max_length=100, null=True)
    buy = models.DecimalField(max_digits=12, decimal_places=2)
    sell = models.DecimalField(max_digits=12, decimal_places=2)
    validate = models.CharField(max_length=100, null=True, blank=True)
    reserve = models.DecimalField(max_digits=12, decimal_places=6)
    is_sell = models.BooleanField(default=True)
    example = models.CharField(max_length=50)
    country = models.CharField(max_length=5, null=True, blank=True)


class AcceptableCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    acceptable = models.ManyToManyField(Currency, related_name='acceptable_currency')


class Wallet(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)


class Exchange(models.Model):
    from_card = models.CharField(max_length=50)
    to_card = models.CharField(max_length=50)
    summa = models.DecimalField(max_digits=12, decimal_places=6)
