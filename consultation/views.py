# consultation/views.py
import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Consultation, ConsultationCategory


@login_required
def book_consultation(request):
    categories = ConsultationCategory.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        category_id = request.POST.get('category')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        message_text = request.POST.get('message', '')

        category = ConsultationCategory.objects.filter(id=category_id).first()

        consultation = Consultation.objects.create(
            user=request.user,
            category=category,
            full_name=full_name,
            phone_number=phone_number,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            message=message_text,
        )

        whatsapp_lines = [
            f"New Consultation Booking #{consultation.id}",
            f"Name: {full_name}",
            f"Phone: {phone_number}",
            f"Category: {category.name if category else 'General'}",
            f"Preferred Date: {preferred_date}",
            f"Preferred Time: {preferred_time}",
        ]
        if message_text:
            whatsapp_lines.append(f"Message: {message_text}")

        whatsapp_message = urllib.parse.quote("\n".join(whatsapp_lines))
        whatsapp_url = f"https://wa.me/{settings.ADMIN_WHATSAPP_NUMBER}?text={whatsapp_message}"

        messages.success(request, "Your consultation request has been saved!")
        return redirect(whatsapp_url)

    return render(request, 'consultation/book.html', {'categories': categories})