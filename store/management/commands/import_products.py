# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand
from store.models import *
import csv
from django.core.files import File
class Command(BaseCommand):
    help = 'Import products from a data file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category_name = row['Category']
                category, _ = Category.objects.get_or_create(name=category_name)
                pdf_path = row['PDF']
                if pdf_path:
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf = File(pdf_file)
                        product_data = {
                            'name': row['Name'],
                            'category': category,
                            'balance': row['Balance'],
                            'type': row['type'],
                            'Info': row['Info'],
                            'price': float(row['Price']),
                            'pdf': pdf,
                            'state': row['State'],
                            'dob': row['DOB'],
                            'gender': row['Gender'],
                        }
                        Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('Products imported successfully.'))


