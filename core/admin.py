# core/admin.py
from django.contrib import admin
from .models import Banner, Testimonial, Announcement, CEOProfile

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_or_location', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    search_fields = ('name', 'message')
    list_editable = ('is_active',)
    ordering = ('-created_at',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    ordering = ('-created_at',)


@admin.register(CEOProfile)
class CEOProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active', 'created_at')
    list_filter = ('is_active',)