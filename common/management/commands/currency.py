
from django.core.management import BaseCommand
from core.models import Currency
import json
from django.conf import settings


class Command(BaseCommand):
    help = "Currency create"

    def handle(self, *args, **options):
        currencies = []
        file_path = settings.BASE_DIR / 'common1/currency.json'
        with open(file_path) as f:
            data = json.load(f)
        for d in data:
            currencies.append(
                Currency(
                    name=d.get("name"),
                    validate=d.get("validate"),
                    example=d.get("example"),
                    min_buy=d.get("min_buy"),
                    is_sell=d.get("is_sell"),
                    is_buy=d.get("is_buy"),
                    reserve=d.get("reserve"),
                    code=d.get('code'),
                    buy=d.get('buy', None),
                    sell=d.get('sell', None),
                )
            )
        Currency.objects.bulk_create(currencies)
