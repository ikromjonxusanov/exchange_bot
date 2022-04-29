from django.contrib import admin
from .models import Currency, AcceptableCurrency, Wallet, Exchange, Excel, CurrencyMinBuy, OwnerCardNumber


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "buy", "sell", 'reserve')
    list_display_links = list_display
    search_fields = ('name',)


@admin.register(CurrencyMinBuy)
class CurrencyMinBuyAdmin(admin.ModelAdmin):
    list_display = ['from_card', 'to_card', 'min_buy_f', 'min_buy_t']
    list_display_links = ['from_card', 'to_card', 'min_buy_f', 'min_buy_t']
    search_fields = ['from_card', 'to_card']


@admin.register(AcceptableCurrency)
class AcceptableCurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('currency', 'number')
    list_display_links = list_display


# @admin.register(Exchange)
# class ExchangeAdmin(admin.ModelAdmin):
#     list_display = ('from_card_number', 'to_card_number', 'give', 'get', 'status')
#     list_display_links = list_display


@admin.register(Excel)
class ExcelAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'name')
    list_display_links = list_display
    readonly_fields = ['file', 'from_user', 'create_at']

    def has_add_permission(self, request):
        return False


@admin.register(OwnerCardNumber)
class OwnerCardNumberAdmin(admin.ModelAdmin):
    list_display = ('currency', 'number')
    list_display_links = list_display
    search_fields = ('number',)
