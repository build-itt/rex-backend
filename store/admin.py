from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'location']
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}

    list_editable = ('slug','location')

admin.site.register(Category, CategoryAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','balance', 'price', 'pdf','Status')
    list_filter = ('name',"price")
    search_fields = ('price','category')
    
    list_editable = ('pdf','balance','price','Status')

    prepopulated_fields ={'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created', 'active','created_by')
    list_filter = ('active', 'created', )
    search_fields = ('name', 'email', 'body','created_by__username')

admin.site.register(Comment, CommentAdmin)