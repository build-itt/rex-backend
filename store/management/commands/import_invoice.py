import csv
from django.core.management.base import BaseCommand
from payment.models import Invoice
from account.models import Customer
from store.models import Product
class Command(BaseCommand):
    help = 'Import invoices from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the input CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = row['status']
                order_id = row['order_id']
                address = row['address']
                btcvalue = row['btcvalue']
                received = row['received']
                created_by = row['created_by']
                product = row['product']
                created_by = Customer.objects.get(user_name=created_by)
                product = Product.objects.filter(name=product).first()
                sold = True
                # Create or update the invoice in the database
                try:
                    Invoice.objects.update_or_create(
                        order_id=order_id,
                        defaults={
                            'status': status,
                            'address': address,
                            'btcvalue': btcvalue,
                            'received': received,
                            'created_by': created_by,
                            'product':product,
                            'sold':sold
                        }
                    )
                except ValueError:
                    btcvalue = 1
                    received = 0
                    Invoice.objects.update_or_create(
                        order_id=order_id,
                        defaults={
                            'status': status,
                            'address': address,
                            'btcvalue': btcvalue,
                            'received': received,
                            'created_by': created_by,
                            'product':product,
                            'sold':sold
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Invoices imported successfully.'))
