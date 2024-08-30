import csv
from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Export categories to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the output CSV file')

    def handle(self, *args, **options):
        categories = Category.objects.all()

        with open(options['file_path'], 'w', newline='') as csvfile:
            fieldnames = ['name', 'slug', 'location', 'number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for category in categories:
                writer.writerow({'name': category.name, 'slug': category.slug, 'location': category.location, 'number': category.number()})

        self.stdout.write(self.style.SUCCESS("Category export complete."))
