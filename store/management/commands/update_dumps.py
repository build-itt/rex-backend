from django.core.management.base import BaseCommand
from store.models import Product, Category
from django.db import transaction
import time # Optional: for timing
import re # Import regular expressions for more robust searching

class Command(BaseCommand):
    help = "Updates the 'Info' field for 'Dumps' category products to alternate TRACK 1/TRACK 2."

    def handle(self, *args, **options):
        start_time = time.time() # Optional: Start timing
        target_category_name = 'Dumps'

        updated_count = 0
        already_correct_count = 0
        no_track_found_count = 0
        skipped_error_count = 0
        batch_size = 1000
        products_batch = []
        fields_to_update = ['Info'] # Only updating Info field

        self.stdout.write(f"Starting alternating TRACK update for products in category '{target_category_name}'...")

        # Use transaction for atomicity
        with transaction.atomic():
            # Fetch products in the target category, only getting pk and Info
            # Using iterator() for memory efficiency
            product_iterator = Product.objects.filter(
                category__name=target_category_name
            ).only('pk', 'Info').select_for_update().iterator() # Fetch only needed fields

            # Use enumerate to get an index for alternating
            for i, product in enumerate(product_iterator):
                info_changed = False
                original_info = product.Info
                new_info = original_info # Start with the original

                # Determine the target TRACK number based on index
                target_track_number = 1 if i % 2 == 0 else 2

                if not original_info or not isinstance(original_info, str):
                     # Skip if Info is None, empty, or not a string
                     self.stdout.write(self.style.NOTICE(f"  Skipping product ID {product.pk}: Info field is empty or not a string."))
                     no_track_found_count += 1 # Count as 'not found' for tracking purposes
                     continue

                try:
                    # Use regex for case-insensitive search and capture the track number
                    match = re.search(r'TRACK\s+(1|2)', original_info, re.IGNORECASE)

                    if match:
                        current_track_number = int(match.group(1))
                        current_track_string = match.group(0) # The full matched string e.g., "TRACK 1"

                        # Check if the current track number needs to be changed
                        if current_track_number != target_track_number:
                            # Construct the replacement string, preserving original case of "TRACK"
                            original_track_word = current_track_string.split()[0]
                            new_track_string = f"{original_track_word} {target_track_number}"

                            # Replace only the first occurrence
                            new_info = original_info.replace(current_track_string, new_track_string, 1)

                            # Verify replacement happened (should always unless original_info was weird)
                            if new_info != original_info:
                                info_changed = True
                                product.Info = new_info # Update the product object
                            else:
                                # Log unexpected no-change scenario
                                self.stdout.write(self.style.WARNING(f"  Product ID {product.pk}: Replacement failed? Original: '{original_info}', Target Track: {target_track_number}"))

                        else:
                            # Track number is already correct for the desired alternating sequence
                            already_correct_count += 1
                            # self.stdout.write(self.style.NOTICE(f"  Product ID {product.pk}: Track number {current_track_number} is already correct for sequence index {i}."))


                    else:
                        # Track 1 or 2 not found in the string
                        self.stdout.write(self.style.NOTICE(f"  Product ID {product.pk}: 'TRACK 1' or 'TRACK 2' not found in Info: '{original_info}'"))
                        no_track_found_count += 1


                    # --- Add to Batch if Info changed ---
                    if info_changed:
                        products_batch.append(product)
                        # updated_count will be incremented when batch succeeds

                except Exception as e:
                     # Catch unexpected errors during processing for a specific product
                     self.stdout.write(self.style.ERROR(f"  Error processing product ID {product.pk}: {e}. Skipping this product."))
                     skipped_error_count += 1
                     continue # Skip this product


                # --- Process Batch ---
                if len(products_batch) >= batch_size:
                    batch_update_start_time = time.time()
                    try:
                        num_in_batch = len(products_batch)
                        Product.objects.bulk_update(products_batch, fields_to_update)
                        updated_count += num_in_batch # Increment count *after* successful update
                        batch_duration = time.time() - batch_update_start_time
                        self.stdout.write(f"  Updated batch of {num_in_batch} products (took {batch_duration:.2f}s).")
                        products_batch = [] # Reset batch
                    except Exception as e:
                         self.stdout.write(self.style.ERROR(f"  Error updating batch: {e}. Skipping batch items."))
                         skipped_error_count += len(products_batch) # Count skipped items
                         products_batch = [] # Reset batch


            # --- Process Final Batch ---
            if products_batch:
                 final_batch_start_time = time.time()
                 try:
                    num_in_batch = len(products_batch)
                    Product.objects.bulk_update(products_batch, fields_to_update)
                    updated_count += num_in_batch # Increment count *after* successful update
                    batch_duration = time.time() - final_batch_start_time
                    self.stdout.write(f"  Updated final batch of {num_in_batch} products (took {batch_duration:.2f}s).")
                 except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Error updating final batch: {e}. Skipping batch items."))
                    skipped_error_count += len(products_batch) # Count skipped items


        end_time = time.time() # Optional: End timing
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f'\nAlternating TRACK update for "{target_category_name}" category complete in {duration:.2f} seconds.'))
        self.stdout.write(self.style.SUCCESS(f'Successfully updated Info field for {updated_count} products.'))
        if already_correct_count > 0:
            self.stdout.write(self.style.NOTICE(f'{already_correct_count} products already had the correct alternating TRACK number.'))
        if no_track_found_count > 0:
             self.stdout.write(self.style.NOTICE(f'{no_track_found_count} products were skipped as "TRACK 1/2" was not found in their Info field (or Info was invalid).'))
        if skipped_error_count > 0:
             self.stdout.write(self.style.WARNING(f'{skipped_error_count} products encountered processing/database errors and were skipped.'))
