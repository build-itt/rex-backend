from django.core.management.base import BaseCommand
from payment.models import Invoice
import csv

class Command(BaseCommand):
    help = 'Export products to a data file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the output data file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['status', 'order_id', 'address', 'btcvalue', 'received',  'created_by','product'])

            for product in Invoice.objects.all():
                writer.writerow([product.status, product.order_id, product.address, product.btcvalue, product.received,  product.created_by, product.product])

        self.stdout.write(self.style.SUCCESS('Invoices exported successfully.'))
