from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

# Клиент моделін тіркеу
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

# CustomUser моделін UserAdmin арқылы тіркеу
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Егер CustomUser-да қосымша өрістер болса, оларды мына жерге қоса аласың:
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('user_type',)}),
    # )
