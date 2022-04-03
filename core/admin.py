from django.contrib import admin
from .models import Currency, AcceptableCurrency, Wallet, Exchange


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "buy", "sell")
    list_display_links = list_display
    search_fields = ('name',)


@admin.register(AcceptableCurrency)
class AcceptableCurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('currency', 'number')
    list_display_links = list_display


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('from_card', 'to_card', 'summa')
    list_display_links = list_display

