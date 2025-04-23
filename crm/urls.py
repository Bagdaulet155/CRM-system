# crm/urls.py
from django.urls import path
from . import views
from django.shortcuts import render
from .models import Client

urlpatterns = [
    path('add_client/', views.add_client, name='add_client'),
    path('client_list/', views.client_list, name='client_list'),
    # Басқа маршруттар
]
