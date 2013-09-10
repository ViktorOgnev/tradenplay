from django.core.management.base import NoArgsCommand
from cart import cart_utils

class Command(NoArgsCommand):
    help = "Delete shopping cart items older than SESSION_AGE_DAYS days"
    def handle_noargs(self, **options):
        cart_utils.remove_old_cart_items()