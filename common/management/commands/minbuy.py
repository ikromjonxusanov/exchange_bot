import json

from django.conf import settings
from django.core.management import BaseCommand

from core.models import Currency, CurrencyMinBuy


class Command(BaseCommand):
    def handle(self, *args, **options):
        MINBUY = []
        file_path = settings.BASE_DIR / 'common/minbuy.json'
        with open(file_path) as f:
            data = json.load(f)

        for item in data:
            from_c = Currency.objects.filter(name__icontains=item.get('from')).first()
            to_c = Currency.objects.filter(name__icontains=item.get('to')).first()
            if from_c and to_c:
                c = CurrencyMinBuy.objects.create(
                    from_card=from_c,
                    to_card=to_c,
                    min_buy_f=item.get('min_buy_f'),
                    min_buy_t=item.get('min_buy_t')
                )
                MINBUY.append(c)
        CurrencyMinBuy.objects.bulk_create(MINBUY)
