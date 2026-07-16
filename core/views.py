from django.shortcuts import render
from products.models import Product
from .models import Banner, Testimonial, Announcement
from django.contrib.auth.decorators import login_required
from orders.models import Order
from consultation.models import Consultation

def home(request):
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_active=True)[:8],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'announcements': Announcement.objects.filter(is_active=True),
    }
    return render(request, 'core/home.html', context)

@login_required
def my_account(request):
    orders = Order.objects.filter(user=request.user)
    consultations = Consultation.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'consultations': consultations,
    }
    return render(request, 'core/my_account.html', context)