import csv
from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Import categories from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the input CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                slug = row['slug']
                location = row['location']
                

                # Create or update the category in the database
                Category.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': name,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Categories imported successfully.'))
