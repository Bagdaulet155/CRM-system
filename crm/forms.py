from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Deal

# Форма для регистрации пользователей
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Форма для создания сделки
class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['client', 'title', 'description', 'amount', 'status', 'document', 'image']