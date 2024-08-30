from django.core.management.base import BaseCommand
from payment.models import Balance
import csv

class Command(BaseCommand):
    help = 'Export products to a data file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the output data file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['status', 'order_id', 'address', 'btcvalue', 'received', 'balance', 'created_by'])

            for product in Balance.objects.all():
                writer.writerow([product.status, product.order_id, product.address, product.btcvalue, product.received, product.balance, product.created_by])

        self.stdout.write(self.style.SUCCESS('Balances exported successfully.'))
