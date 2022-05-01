from django.core.management import BaseCommand
import logging
from warnings import filterwarnings
from core.dispatcher import main
filterwarnings(action="ignore", message=r".*CallbackQueryHandler")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Telegram handlers"

    def handle(self, *args, **options):
        main()
