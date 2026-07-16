# consultation/admin.py
from django.contrib import admin
from .models import ConsultationCategory, Consultation

@admin.register(ConsultationCategory)
class ConsultationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'preferred_date', 'preferred_time', 'status', 'phone_number', 'created_at')
    list_filter = ('status', 'category', 'preferred_date')
    search_fields = ('full_name', 'phone_number', 'user__username')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)