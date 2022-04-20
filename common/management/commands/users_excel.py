from datetime import datetime

from django.core.management import BaseCommand
from account.models import BotUser
from common.service import get_user_for_excel


class Command(BaseCommand):
    help = "Users data for excel"

    def handle(self, *args, **options):
        print(datetime.now())
        get_user_for_excel("test.xlsx")
        print(datetime.now())
