from django.contrib import admin
from .models import *
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('created_by','product', 'sold',)
    list_filter = ('sold',)
    search_fields = ('created_by__username',)
    
    list_editable = ('sold','product')

admin.site.register(Invoice, InvoiceAdmin)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ( 'created_by', 'address', 'balance')
    
    search_fields = ('created_by__username',)
    
    list_editable = ('balance',)

admin.site.register(Balance, BalanceAdmin)

class Telegram_ClientAdmin(admin.ModelAdmin):
    list_display = ( 'order_id', 'address', 'balance', 'received', 'chat_id','created_at')
    
    search_fields = ('chat_id',)
    
    list_editable = ('balance',)

    fieldsets = (
        (None, {
            'fields': ( 'order_id', 'address', 'received', 'balance', 'chat_id',)
        }),
    )
#admin.site.register(Telegram_Client, Telegram_ClientAdmin)

class Telegram_Otp_botAdmin(admin.ModelAdmin):
    list_display = ( 'order_id', 'address', 'name', 'log', 'chat_id','created_at','number','trial_used',)
    
    search_fields = ('chat_id',)
    
    list_editable = ('number','trial_used',)

    fieldsets = (
        (None, {
            'fields': ( 'order_id', 'address', 'received', 'balance', 'chat_id','name','number','log','trial_used','otp_code')
        }),
    )
#admin.site.register(Telegram_Otp_bot, Telegram_Otp_botAdmin)
admin.site.register(Addr)