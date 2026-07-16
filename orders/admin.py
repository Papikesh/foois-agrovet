# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone_number', 'user__username')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total'