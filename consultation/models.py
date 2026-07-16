from django.db import models
from django.conf import settings

class ConsultationCategory(models.Model):
    """e.g. Soil Testing, Crop Advisory, Pest Control"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations')
    category = models.ForeignKey(ConsultationCategory, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, help_text="Any details the user wants to share upfront")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.category} ({self.status})"