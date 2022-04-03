import json
from django.conf import settings
from django.core.management import BaseCommand
from core.models import Currency


class Command(BaseCommand):

    def handle(self, *args, **options):
        currencies = []
        file_path = settings.BASE_DIR / 'common/currency.json'
        data = []
        with open(file_path) as f:
            data = json.load(f)

        for d in data:
            pass



