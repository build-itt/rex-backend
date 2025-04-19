from django.core.management.base import BaseCommand
from django.db import transaction
from store.models import Category
import time # Optional: for timing

class Command(BaseCommand):
    help = 'Updates the location for existing Category objects based on predefined bank lists.'

    # No need for add_arguments since we don't take a file path

    def handle(self, *args, **options):
        start_time = time.time() # Optional: Start timing

        # --- Bank Lists ---
        CANADIAN_BANKS = [
            "Royal Bank of Canada (RBC)", "Toronto-Dominion Bank (TD)",
            "Bank of Nova Scotia (Scotiabank)", "Bank of Montreal (BMO)",
            "Canadian Imperial Bank of Commerce (CIBC)", "National Bank of Canada",
            "Desjardins Group", "Laurentian Bank of Canada", "HSBC Bank Canada",
            "Canadian Western Bank", "Tangerine Bank", "EQ Bank",
            "Manulife Bank of Canada", "Simplii Financial", "ATB Financial"
        ]

        UK_BANKS = [
            "HSBC Holdings PLC", "Barclays PLC", "Lloyds Banking Group PLC",
            "NatWest Group PLC", "Standard Chartered PLC", "Santander UK PLC",
            "Nationwide Building Society", "TSB Bank PLC", "Metro Bank PLC",
            "Clydesdale Bank PLC", "Virgin Money UK PLC", "Co-operative Bank PLC",
            "Monzo Bank Limited", "Starling Bank Limited", "Revolut Ltd"
        ]

        updated_ca_count = 0
        updated_uk_count = 0
        not_found_banks = []

        self.stdout.write("Starting category location update...")

        # Use a transaction for efficiency and atomicity
        with transaction.atomic():
            # Update Canadian Banks
            self.stdout.write("Updating Canadian bank categories...")
            for bank_name in CANADIAN_BANKS:
                # Find categories matching the name and update their location
                num_updated = Category.objects.filter(name=bank_name).update(location='Canada')
                if num_updated > 0:
                    updated_ca_count += num_updated
                    self.stdout.write(self.style.SUCCESS(f"  Updated {num_updated} category(ies) for '{bank_name}' to location 'Canada'."))
                else:
                     # Check if the category exists at all
                     if not Category.objects.filter(name=bank_name).exists():
                         not_found_banks.append(f"{bank_name} (Canada)")
                         self.stdout.write(self.style.WARNING(f"  No category found with name '{bank_name}'."))
                     else:
                         # Category exists but location might already be correct
                         self.stdout.write(self.style.NOTICE(f"  Category '{bank_name}' already exists (possibly with correct location)."))


            # Update UK Banks
            self.stdout.write("Updating UK bank categories...")
            for bank_name in UK_BANKS:
                # Find categories matching the name and update their location
                num_updated = Category.objects.filter(name=bank_name).update(location='UK')
                if num_updated > 0:
                    updated_uk_count += num_updated
                    self.stdout.write(self.style.SUCCESS(f"  Updated {num_updated} category(ies) for '{bank_name}' to location 'United Kingdom'."))
                else:
                    if not Category.objects.filter(name=bank_name).exists():
                         not_found_banks.append(f"{bank_name} (UK)")
                         self.stdout.write(self.style.WARNING(f"  No category found with name '{bank_name}'."))
                    else:
                         self.stdout.write(self.style.NOTICE(f"  Category '{bank_name}' already exists (possibly with correct location)."))


        end_time = time.time() # Optional: End timing
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(
            f'\nCategory location update complete in {duration:.2f} seconds.'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total Canadian categories updated/verified: {updated_ca_count}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total UK categories updated/verified: {updated_uk_count}'
        ))

        if not_found_banks:
             self.stdout.write(self.style.WARNING(
                 "\nWarning: The following banks were listed but no matching category name was found in the database:"
             ))
             for bank in not_found_banks:
                 self.stdout.write(self.style.WARNING(f"  - {bank}"))
