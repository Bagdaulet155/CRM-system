from django.contrib import admin
from .models import Client
from .models import CustomUser


# Регистрируем модель Client в админке
admin.site.register(Client)

admin.site.register(CustomUser)
