import random
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Randomize product prices for all products with proportional scaling and ensure total balance does not exceed 10000'

    def handle(self, *args, **options):
        # Define the price range and max total balance
        price_min = 250
        price_max = 500
        balance_min = 4000
        balance_max = 19000
        

        # Get all products
        products = Product.objects.filter(category__location='Canada')

        for product in products:
            # Calculate price based on product balance
            try:
                balance = float(product.Balance)
            except ValueError:
                balance = 10000  # Assuming the balance is a field in Product model
            price = price_min + (price_max - price_min) * ((balance - balance_min) / (balance_max - balance_min))
            price = round(price)  # Round to nearest integer

            product.price = price
            product.save()
            

        self.stdout.write(self.style.SUCCESS('Prices randomized successfully.'))

