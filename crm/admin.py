from django.contrib import admin
from .models import Client

# Регистрируем модель Client в админке
admin.site.register(Client)
