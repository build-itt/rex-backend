# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand
from store.models import Product, Category  # Update 'store' to your app name
import csv
from django.utils.text import slugify
from django.core.files import File
from django.db import transaction

class Command(BaseCommand):
    help = "Import products from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        
        # Use transaction to make the process faster
        with transaction.atomic():
            # Pre-fetch all categories to avoid repeated database queries
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                # Get unique category names from the CSV
                category_names = set(row["Category"] for row in reader)
            
            # Skip header row
            
            # Get or create all categories at once
            categories = {}
            existing_categories = {cat.name: cat for cat in Category.objects.filter(name__in=category_names)}
            
            # Get all existing slugs to check for uniqueness
            existing_slugs = set(Category.objects.values_list('slug', flat=True))
            
            # Create any missing categories with bulk_create
            categories_to_create = []
            for name in category_names:
                if name not in existing_categories:
                    # Create a unique slug
                    base_slug = slugify(name)
                    unique_slug = base_slug
                    counter = 1
                    
                    # If slug exists, append a number until we get a unique one
                    while unique_slug in existing_slugs:
                        unique_slug = f"{base_slug}-{counter}"
                        counter += 1
                    
                    # Add the unique slug to our tracking set
                    existing_slugs.add(unique_slug)
                    
                    categories_to_create.append(Category(
                        name=name,
                        slug=unique_slug
                    ))
            
            if categories_to_create:
                created_categories = Category.objects.bulk_create(categories_to_create)
                # Update our categories dictionary with newly created ones
                for category in created_categories:
                    existing_categories[category.name] = category
            
            # Now process products in bulk
            products_to_create = []
            
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Get category from our pre-fetched dictionary
                    category = existing_categories[row["Category"]]
                    
                    # Handle optional PDF field
                    pdf = None
                    pdf_path = row.get("pdf")
                    if pdf_path:
                        try:
                            with open(pdf_path, "rb") as pdf_file:
                                pdf = File(pdf_file)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"Could not process PDF '{pdf_path}': {str(e)}"))
                    
                    # Create product object (without saving to DB yet)
                    product = Product(
                        category=category,
                        name=row["Name"],
                        bin=row.get("Bin", ""),
                        zip=row.get("Zip", ""),
                        exp=row.get("Exp", ""),
                        country=row.get("Country", ""),
                        bank=row.get("Bank", ""),
                        balance=row.get("Balance", ""),
                        type=row.get("type", ""),
                        Info=row.get("Info", ""),
                        slug=slugify(row["Name"]),
                        price=float(row.get("Price", 0.0)),
                        state=row.get("State", ""),
                        gender=row.get("Gender", ""),
                        dob=row.get("DOB", ""),
                        Status=bool((row.get("Status", 1))),
                        pdf=pdf,
                    )
                    
                    products_to_create.append(product)
                    
                    # Process in batches of 1000 to avoid memory issues
                    if len(products_to_create) >= 1000:
                        Product.objects.bulk_create(products_to_create)
                        products_to_create = []
                        self.stdout.write(self.style.SUCCESS('Batch of 1000 products imported.'))
            
            # Create any remaining products
            if products_to_create:
                Product.objects.bulk_create(products_to_create)
        
        self.stdout.write(self.style.SUCCESS('All products imported successfully.'))