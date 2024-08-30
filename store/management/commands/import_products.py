# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand
from store.models import *
import csv
import random
from django.core.files import File
from django.utils.text import slugify
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
                slug = slugify(row['Name']+str(random.randint(1,1000000)))
                location = row['Location']
                category, _ = Category.objects.get_or_create(name=category_name,location=location)
                try:
                    pdf_path = row['PDF']
                except:
                    pdf_path = None
                if pdf_path:
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf = File(pdf_file)
                        product_data = {
                            'name': row['Name'],
                            'category': category,
                            'Balance': row['Balance'],
                            'Title': row['Title'],
                            'Info': row['Info'],
                            'price': float(row['Price']),
                            'slug': slug,
                            'pdf': pdf,
                        }
                        Product.objects.create(**product_data)
                else:
                    product_data = {
                        'name': row['Name'],
                        'category': category,
                        'Balance': row['Balance'],
                        'Title': row['Title'],
                        'Info': row['Info'],
                        'price': float(row['Price']),
                        'slug': slug,
                    }
                    Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('Products imported successfully.'))



