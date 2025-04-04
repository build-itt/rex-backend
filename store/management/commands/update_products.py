from django.core.management.base import BaseCommand
from store.models import Product
import random
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q

class Command(BaseCommand):
    help = 'Update products from a data file'

    def handle(self, *args, **options):
        products = Product.objects.all()
        
        for product in products:
            number_str = str(product.balance)
            if '.' in number_str:
                decimal_part = number_str.split('.')[1]
                dp=len(decimal_part)
                if dp > 2:
                    product.balance = str(round(float(product.balance),2))
                    product.save()
        
        # Define US states for random assignment
        states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]
        
        # Generate random date between 1960 and 1987
        def random_dob():
            start_date = datetime(1960, 1, 1)
            end_date = datetime(1987, 12, 31)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            return random_date.strftime('%Y-%m-%d')
        
        # Perform bulk update for empty fields
        with transaction.atomic():
            # Get products with empty fields
            products_to_update = Product.objects.filter(
                Q(dob__in=['', None]) | 
                Q(state__in=['', None]) | 
                Q(gender__in=['', None])
            )
            
            self.stdout.write(f"Found {products_to_update.count()} products to update")
            
            # Process in batches for efficiency
            batch_size = 1000
            products_list = list(products_to_update)
            updated_products = []
            
            for i, product in enumerate(products_list):
                # Alternate gender between M and F
                if not product.gender:
                    product.gender = 'M' if i % 2 == 0 else 'F'
                
                # Set random state if empty
                if not product.state:
                    product.state = random.choice(states)
                
                # Set random DOB if empty
                if not product.dob:
                    product.dob = random_dob()
                
                updated_products.append(product)
                
                # Bulk update in batches
                if len(updated_products) >= batch_size:
                    Product.objects.bulk_update(updated_products, ['gender', 'state', 'dob'])
                    self.stdout.write(f"Updated batch of {len(updated_products)} products")
                    updated_products = []
            
            # Update any remaining products
            if updated_products:
                Product.objects.bulk_update(updated_products, ['gender', 'state', 'dob'])
                self.stdout.write(f"Updated final batch of {len(updated_products)} products")
                
        self.stdout.write(self.style.SUCCESS('Products updated successfully.'))
