from django.core.management.base import BaseCommand
from store.models import Product, Category
import random
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
import decimal

class Command(BaseCommand):
    help = 'Updates product balances, countries based on category, and empty DOB/State/Gender fields.'

    def handle(self, *args, **options):

        # --- 1. Balance Update ---
        # Consider making this more efficient if possible (e.g., bulk_update)
        # but it requires fetching and checking each value currently.
        self.stdout.write("Checking and updating product balances (rounding)...")
        balance_updated_count = 0
        # Use iterator() for memory efficiency if dealing with many products
        products_for_balance = Product.objects.all().iterator()
        products_to_save_balance = [] # Collect products needing save

        # Note: This part still saves one by one, which can be slow.
        # If performance is critical, explore raw SQL or more complex bulk logic.
        for product in products_for_balance:
            try:
                # Ensure balance is treated as Decimal
                balance_str = str(product.balance)
                balance_decimal = decimal.Decimal(balance_str)

                # Check number of decimal places
                if balance_decimal.as_tuple().exponent < -2:
                    rounded_balance = balance_decimal.quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_UP)
                    product.balance = rounded_balance # Update with Decimal
                    # Don't save here, update later if needed or rethink approach
                    # For now, keeping the original save logic for simplicity
                    product.save() # Original logic saved here
                    balance_updated_count += 1

            except (decimal.InvalidOperation, ValueError, TypeError) as e:
                 self.stdout.write(self.style.WARNING(f"  Skipping balance update for product ID {product.pk}: Invalid balance value '{product.balance}' ({e})"))
            except Exception as e:
                 self.stdout.write(self.style.ERROR(f"  Unexpected error updating balance for product ID {product.pk}: {e}"))

        if balance_updated_count > 0:
             self.stdout.write(self.style.SUCCESS(f"Rounded balances for {balance_updated_count} products."))
        else:
             self.stdout.write(self.style.NOTICE("No product balances required rounding."))


        # --- Define states and DOB function ---
        states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]

        def random_dob():
            start_date = datetime(1960, 1, 1)
            end_date = datetime(1987, 12, 31)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            return random_date.strftime('%Y-%m-%d')

        # --- Perform updates within a single transaction ---
        with transaction.atomic():

            # --- 2. Update Country based on Category Location ---
            self.stdout.write("Updating product countries based on category locations...")

            # Set target country values (ensure these match your desired standard)
            canada_country = 'Canada'
            uk_country = 'United Kingdom' # Match value used in import_category

            # Update Canada Products
            updated_ca_country_count = Product.objects.filter(
                category__location=canada_country # Filter by category's location
            ).exclude(
                country=canada_country # Only update if country isn't already correct
            ).update(country=canada_country) # Set the product's country

            if updated_ca_country_count > 0:
                 self.stdout.write(self.style.SUCCESS(f"  Set country to '{canada_country}' for {updated_ca_country_count} products."))

            # Update UK Products
            updated_uk_country_count = Product.objects.filter(
                category__location=uk_country
            ).exclude(
                country=uk_country
            ).update(country=uk_country)

            if updated_uk_country_count > 0:
                 self.stdout.write(self.style.SUCCESS(f"  Set country to '{uk_country}' for {updated_uk_country_count} products."))

            self.stdout.write("Product country update based on category finished.")


            # --- 3. DOB/State/Gender Update (using bulk_update) ---
            self.stdout.write("Updating products with empty DOB/State/Gender...")

            # Get products with empty fields - use only() to fetch only needed fields + pk
            products_to_update_qs = Product.objects.filter(
                Q(dob__in=['', None]) |
                Q(state__in=['', None]) |
                Q(gender__in=['', None])
            ).only('pk', 'gender', 'state', 'dob') # Fetch only necessary fields

            count_to_update = products_to_update_qs.count() # Get count before iterating
            self.stdout.write(f"Found {count_to_update} products with empty fields to potentially update.")

            batch_size = 1000
            updated_in_batch_count = 0

            # Use .iterator() for memory efficiency
            for i, product in enumerate(products_to_update_qs.iterator()):
                update_needed = False
                # Alternate gender between M and F
                if not product.gender:
                    product.gender = 'M' if i % 2 == 0 else 'F'
                    update_needed = True

                # Set random state if empty
                if not product.state:
                    product.state = random.choice(states)
                    update_needed = True

                # Set random DOB if empty
                if not product.dob:
                    product.dob = random_dob()
                    update_needed = True

                if update_needed:
                    # Add to list for bulk update
                    # We don't need a separate list, we can update in batches directly
                    # This part needs restructuring for bulk_update

                     # ---- Re-structuring for bulk_update ----
                     # This section needs to collect objects and then call bulk_update outside the loop
                     # Or update in batches as originally intended. Let's stick to the batch approach.

                     # The original batch logic was slightly flawed. Let's refine.
                     # We need to collect a batch *of objects that changed*.

                     pass # Placeholder - Original batch logic below needs refinement

            # --- Refining the original batch logic ---
            products_list_for_bulk = []
            fields_to_update = ['gender', 'state', 'dob']
            total_bulk_updated = 0

            # Re-iterate specifically for bulk update preparation
            # This is less efficient than doing it in one pass, but simpler to implement based on original structure
            products_to_update_qs = Product.objects.filter(
                 Q(dob__in=['', None]) |
                 Q(state__in=['', None]) |
                 Q(gender__in=['', None])
             ) # Re-fetch queryset

            for i, product in enumerate(products_to_update_qs.iterator()):
                 changed = False
                 if not product.gender:
                     product.gender = 'M' if i % 2 == 0 else 'F'
                     changed = True
                 if not product.state:
                     product.state = random.choice(states)
                     changed = True
                 if not product.dob:
                     product.dob = random_dob()
                     changed = True

                 if changed:
                     products_list_for_bulk.append(product)

                 # Process batch
                 if len(products_list_for_bulk) >= batch_size:
                     Product.objects.bulk_update(products_list_for_bulk, fields_to_update)
                     self.stdout.write(f"  Updated batch of {len(products_list_for_bulk)} products (DOB/State/Gender).")
                     total_bulk_updated += len(products_list_for_bulk)
                     products_list_for_bulk = [] # Reset batch

            # Update any remaining products in the last batch
            if products_list_for_bulk:
                Product.objects.bulk_update(products_list_for_bulk, fields_to_update)
                self.stdout.write(f"  Updated final batch of {len(products_list_for_bulk)} products (DOB/State/Gender).")
                total_bulk_updated += len(products_list_for_bulk)

            self.stdout.write(f"Finished DOB/State/Gender updates. Total products updated in this step: {total_bulk_updated}.")
            # ---- End refined batch logic ----


        self.stdout.write(self.style.SUCCESS('\nProduct updates completed successfully.'))
