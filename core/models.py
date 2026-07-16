# core/models.py
from django.db import models

class Banner(models.Model):
    """Hero/carousel images on the homepage"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    link_url = models.URLField(blank=True, help_text="Where the banner button/click leads, if anywhere")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer reviews shown on the homepage"""
    name = models.CharField(max_length=150)
    role_or_location = models.CharField(max_length=150, blank=True, help_text="e.g. 'Farmer, Ogun State' or leave blank")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class Announcement(models.Model):
    """Site-wide banners/notices, e.g. 'New stock arriving Friday!'"""
    text = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text