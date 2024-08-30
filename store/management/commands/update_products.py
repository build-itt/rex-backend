from django.core.management.base import BaseCommand
from store.models import Product
import random

class Command(BaseCommand):
    help = 'Update products from a data file'


    def handle(self, *args, **options):
        products = Product.objects.filter(category__location='Canada')
        
        for product in products:
            number_str = str(product.Balance)
            if '.' in number_str:
                decimal_part = number_str.split('.')[1]
                dp=len(decimal_part)
            if dp > 2:
                product.Balance = str(round(float(product.Balance),2))
                product.save()
        self.stdout.write(self.style.SUCCESS('Products updated successfully.'))
