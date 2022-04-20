from django.contrib import admin
from .models import Currency, AcceptableCurrency, Wallet, Exchange, Excel


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "buy", "sell", 'reserve')
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


@admin.register(Excel)
class ExcelAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'name')
    list_display_links = list_display
    readonly_fields = ['file', 'from_user', 'create_at']

    def has_add_permission(self, request):
        return False
