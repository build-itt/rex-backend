from rest_framework import serializers
from .models import Balance, Invoice, Telegram_Client, Telegram_Otp_bot
from store.serializers import ProductSerializer

class BalanceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Balance
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    product = ProductSerializer()
    class Meta:
        model = Invoice
        fields = ['id','created_by','received','product','decrypted']

class Telegram_ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram_Client
        fields = '__all__'
    
class Telegram_OtpBotserializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram_Otp_bot
        fields = '__all__'