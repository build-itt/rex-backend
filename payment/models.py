from django.db import models
from store.models import Product
from accounts.models import Customer
from django.utils import timezone
class Invoice(models.Model):
    STATUS_CHOICES = ((-1,"Not Started"),(0,'Unconfirmed'), (1,"Partially Confirmed"), (2,"Confirmed"))

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=-1)
    order_id = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True, null=True)
    btcvalue = models.FloatField(blank=True, null=True)
    received = models.FloatField(blank=True, null=True)
    txid = models.CharField(max_length=250, blank=True, null=True)
    rbf = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now,blank=True, null=True)
    created_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    decrypted = models.BooleanField(default=False)
    def __str__(self):
        return self.product.name
    
class Balance(models.Model):
    order_id = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True, null=True)
    received = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    txid = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.created_by.username

class Telegram_Client(models.Model):
    order_id = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True, null=True)
    received = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    txid = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    chat_id = models.CharField(max_length=250)
    
    def __str__(self):
        return self.chat_id

class Telegram_Otp_bot(models.Model):
    order_id = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True, null=True)
    received = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    otp_code = models.CharField(max_length=50,blank=True, null=True)
    txid = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    chat_id = models.CharField(max_length=250)
    number = models.CharField(max_length=50,blank=True,null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    log = models.BooleanField(default=False)
    trial_used = models.BooleanField(default=False)
    def __str__(self):
        return self.chat_id

class Addr(models.Model):
    address = models.CharField(max_length=250)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.created_by.username