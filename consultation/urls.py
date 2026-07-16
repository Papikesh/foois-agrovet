# consultation/urls.py
from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('', views.book_consultation, name='book'),
]