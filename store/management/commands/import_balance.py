import csv
from django.core.management.base import BaseCommand
from payment.models import Balance
from account.models import Customer
class Command(BaseCommand):
    help = 'Import balances from a CSV file'

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
                balance = row['balance']
                created_by = row['created_by']
                created_by = Customer.objects.get(user_name=created_by)
                # Create or update the balance in the database
                try:
                    Balance.objects.update_or_create(
                        order_id=order_id,
                        defaults={
                            'status': status,
                            'address': address,
                            'btcvalue': btcvalue,
                            'received': received,
                            'balance': balance,
                            'created_by': created_by
                        }
                    )
                except ValueError:
                    received = 0
                    balance = 0
                    Balance.objects.update_or_create(
                        order_id=order_id,
                        defaults={
                            'status': status,
                            'address': address,
                            'btcvalue': btcvalue,
                            'received': received,
                            'balance': balance,
                            'created_by': created_by
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Balances imported successfully.'))
