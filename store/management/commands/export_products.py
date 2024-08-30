from django.core.management.base import BaseCommand
from store.models import Product
import csv

class Command(BaseCommand):
    help = 'Export products to a data file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the output data file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Name', 'Balance', 'Title', 'Info', 'Slug', 'Price', 'Status',  'PDF'])

            for product in Product.objects.all():
                writer.writerow([product.category, product.name, product.Balance, product.Title, product.Info, product.slug, product.price, product.Status, product.pdf])

        self.stdout.write(self.style.SUCCESS('Products exported successfully.'))
