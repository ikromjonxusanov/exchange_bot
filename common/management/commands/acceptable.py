from django.core.management import BaseCommand
from core.models import Currency, AcceptableCurrency
import json
from django.conf import settings


class Command(BaseCommand):
    help = "Currency create"

    def handle(self, *args, **options):
        acceptablecurrencies = []
        file_path = settings.BASE_DIR / 'common/acceptable.json'
        with open(file_path) as f:
            datas = json.load(f)

        for data in datas:
            c_name = data.get('name')
            currency = Currency.objects.filter(name__icontains=c_name).first()
            if currency:
                acceptablecurrency = AcceptableCurrency(currency=currency)
                acceptablecurrencies.append(acceptablecurrency)
        AcceptableCurrency.objects.bulk_create(acceptablecurrencies)
        for data in datas:
            c_name = data.get('name')
            currency = Currency.objects.filter(name__icontains=c_name).first()
            if currency:
                acceptablecurrency = AcceptableCurrency.objects.filter(currency=currency).first()
                for name in data.get("items", []):
                    ac_currency = Currency.objects.filter(name__icontains=name).first()
                    if ac_currency:
                        acceptablecurrency.acceptable.add(ac_currency)
                acceptablecurrency.save()
