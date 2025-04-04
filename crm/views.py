from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from .models import Client, Deal
from .forms import SignUpForm, DealForm, ClientForm
from django.contrib.auth.decorators import login_required
# Представление для регистрации пользователя
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически авторизуем пользователя после регистрации
            return redirect('client_list')  # Перенаправляем на список клиентов после регистрации
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Представление для входа пользователя (с использованием встроенной Django формы)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Главная страница (домашняя)
def home(request):
    return render(request, 'home.html')

# Список клиентов
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'crm/client_list.html', {'clients': clients})

# Представление для создания сделки
def create_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deal_list')  # Перенаправляем на список сделок
    else:
        form = DealForm()
    return render(request, 'crm/create_deal.html', {'form': form})

# Список сделок
def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'crm/deal_list.html', {'deals': deals})