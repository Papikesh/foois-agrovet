# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'in_stock', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    ordering = ('-created_at',)

    def in_stock(self, obj):
        return obj.in_stock
    in_stock.boolean = True
    in_stock.short_description = 'In Stock?'