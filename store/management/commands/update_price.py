import random
from django.core.management.base import BaseCommand
from store.models import Product
from django.db import transaction
import decimal # Import decimal

class Command(BaseCommand):
    help = 'Generates new random balances (10k-110k) and calculates new prices (300 + Balance/100) for ALL products.'

    def handle(self, *args, **options):
        # --- Parameters for Balance Generation ---
        # Use Decimal for balance range
        MIN_BALANCE = decimal.Decimal('10000.00')
        MAX_BALANCE = decimal.Decimal('110000.00') # Exclusive upper bound

        # --- Parameters for Price Calculation ---
        BASE_PRICE = decimal.Decimal('300.00')
        PRICE_BALANCE_FACTOR = decimal.Decimal('100.00')

        # --- Decimal Context ---
        ctx = decimal.Context(rounding=decimal.ROUND_HALF_UP)
        # Optional: Adjust precision if needed
        # decimal.getcontext().prec = 28

        # --- Counters and Batching ---
        processed_count = 0
        error_count = 0
        batch_size = 1000
        products_batch = []
        fields_to_update = ['balance', 'price'] # Always update both

        self.stdout.write("Starting generation of new balances and prices for all products...")

        # Use transaction for atomicity
        with transaction.atomic():
            # Iterate over ALL products
            # Use iterator() for memory efficiency and only fetch pk initially
            product_iterator = Product.objects.all().only('pk').select_for_update().iterator()

            for product in product_iterator:
                try:
                    # --- 1. Generate New Random Balance ---
                    # Use random.uniform with float conversion, then convert back to Decimal
                    balance_float = random.uniform(float(MIN_BALANCE), float(MAX_BALANCE))
                    new_balance_decimal = ctx.create_decimal(balance_float)
                    product.balance = new_balance_decimal.quantize(decimal.Decimal("0.01"), context=ctx)

                    # --- 2. Calculate New Price based on NEW Balance ---
                    # Price = BASE_PRICE + (new_balance / PRICE_BALANCE_FACTOR)
                    calculated_price = BASE_PRICE + (product.balance / PRICE_BALANCE_FACTOR)
                    product.price = calculated_price.quantize(decimal.Decimal("0.01"), context=ctx)

                    # --- Add to Batch ---
                    # Since we are generating new values for all, always add
                    products_batch.append(product)
                    processed_count += 1 # Count products prepared for update

                except Exception as e:
                     # Catch any unexpected error during generation/calculation for a product
                     self.stdout.write(self.style.ERROR(f"  Error processing product ID {product.pk}: {e}. Skipping this product."))
                     error_count += 1
                     continue # Skip this product


                # --- Process Batch ---
                if len(products_batch) >= batch_size:
                    try:
                        # Update both fields for all items in the batch
                        Product.objects.bulk_update(products_batch, fields_to_update)
                        self.stdout.write(f"  Updated batch of {len(products_batch)} products.")
                        products_batch = [] # Reset batch
                    except Exception as e:
                         self.stdout.write(self.style.ERROR(f"  Error updating batch: {e}. Skipping batch items."))
                         # Items in this failed batch won't be counted in final success counts
                         error_count += len(products_batch) # Count skipped items
                         products_batch = [] # Reset batch


            # --- Process Final Batch ---
            if products_batch:
                 try:
                    Product.objects.bulk_update(products_batch, fields_to_update)
                    self.stdout.write(f"  Updated final batch of {len(products_batch)} products.")
                 except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Error updating final batch: {e}. Skipping batch items."))
                    error_count += len(products_batch) # Count skipped items


        self.stdout.write(self.style.SUCCESS(f'\nNew Balance and Price generation complete.'))
        # Calculate success count based on processed minus errors during batch updates
        success_count = processed_count - error_count
        self.stdout.write(self.style.SUCCESS(f'Successfully generated and saved new balances/prices for {success_count} products.'))
        if error_count > 0:
             self.stdout.write(self.style.WARNING(f'{error_count} products encountered errors and were skipped.'))
