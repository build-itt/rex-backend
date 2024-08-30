from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    '''Admin View for Customer'''

    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active',)  # Make sure to use a tuple with a comma at the end
    list_editable = ('is_active',)
    readonly_fields = ('email',)  # Make sure to use a tuple with a comma at the end
    search_fields = ('username','email',)
