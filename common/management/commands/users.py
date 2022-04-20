import random
import string
from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from account.models import BotUser
# from common.service import get_user_for_excel


def name_generator():
    return "".join([random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 15))])


def fullname_generator():
    return name_generator() + " " + name_generator()


class Command(BaseCommand):
    help = "Users data for excel"

    def handle(self, *args, **options):
        users = []
        for _ in range(5000):
            try:
                users.append(
                    BotUser(
                        tg_id=random.randint(10000000000000, 99999999999999),
                        full_name=fullname_generator(),
                        phone=random.randint(1000000000000, 9999999999999),
                        is_active=True,
                        lang=random.choice(['uz', 'ru'])
                    )
                )
            except IntegrityError:
                users.append(
                    BotUser(
                        tg_id=random.randint(10000000000000, 99999999999999),
                        full_name=fullname_generator(),
                        phone=random.randint(1000000000000, 9999999999999),
                        is_active=True,
                        lang=random.choice(['uz', 'ru'])
                    )
                )

        # BotUser.objects.order_by("-pk").filter(is_active=True).delete()

        BotUser.objects.bulk_create(users)
