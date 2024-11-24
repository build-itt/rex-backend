# myapp/management/commands/import_products.py

from django.core.management.base import BaseCommand
from store.models import Product, Category  # Update 'store' to your app name
import csv
from django.utils.text import slugify
from django.core.files import File

class Command(BaseCommand):
    help = "Import products from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        file_path = options["file_path"]

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get or create category
                category_name = row["category"]
                category, _ = Category.objects.get_or_create(name=category_name)

                # Handle optional PDF field
                pdf_path = row.get("pdf")
                pdf = None
                if pdf_path:
                    try:
                        with open(pdf_path, "rb") as pdf_file:
                            pdf = File(pdf_file)
                    except FileNotFoundError:
                        self.stdout.write(self.style.WARNING(f"PDF not found: {pdf_path}"))

                # Prepare product data
                product_data = {
                    "category": category,
                    "name": row["name"],
                    "bin": row["bin"],
                    "zip": row["zip"],
                    "exp": row["exp"],
                    "country": row["country"],
                    "bank": row["bank"],
                    "balance": row.get("balance", ""),  # Optional field
                    "type": row["type"],
                    "Info": row["Info"],
                    "slug": slugify(row["name"]),  # Generate slug
                    "price": float(row.get("price", 0.0)),  # Default to 0.0 if not provided
                    "state": row["state"],
                    "gender": row.get("gender", ""),  # Optional field
                    "dob": row.get("dob", ""),  # Optional field
                    "Status": bool(int(row.get("Status", 1))),  # Default to True
                    "pdf": pdf,
                }

                # Create or update the product
                Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('Products imported successfully.'))