from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('my-account/', views.my_account, name='my_account'),
    path('meet-the-ceo/', views.meet_the_ceo, name='meet_the_ceo'),
]