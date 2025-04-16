from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests
from datetime import datetime
from django.conf import settings
from .models import Client, Deal
from .forms import SignUpForm, DealForm, SomeForm  # Импортируем формы
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from django.contrib.auth import get_user_model  # get_user_model() импорттау
User = get_user_model() 


def some_view(request):
    if request.method == 'POST':
        form = SomeForm(request.POST)
        if form.is_valid():
            # Если форма заполнена правильно, выполните какое-то действие
            messages.success(request, 'Форма успешно отправлена!')
        else:
            # Если в форме есть ошибки
            messages.error(request, 'В форме есть ошибки!')
    else:
        form = SomeForm()

    return render(request, 'some_template.html', {'form': form})


@require_http_methods(["GET", "POST"])  # Ограничение методов
@login_required
def sensitive_action(request):
    # Ваш код для защищённого действия
    pass


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        # ✅ reCAPTCHA тексеру
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if settings.RECAPTCHA_SECRET_KEY and recaptcha_response:
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if not result.get('success'):
                form.add_error(None, 'reCAPTCHA validation failed. Please try again.')

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Тіркелу сәтті өтті!")
            return redirect('home')
        else:
            messages.error(request, "Формада қателер бар. Тексеріңіз.")
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'crm/client_list.html', {'clients': clients})


@login_required
def deal_list(request):
    deals = Deal.objects.all()
    clients = Client.objects.all()

    # Параметрлерді алу
    client_id = request.GET.get('client')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    sort_by = request.GET.get('sort_by')

    # Фильтрация
    if client_id:
        deals = deals.filter(client__id=client_id)

    if min_amount:
        deals = deals.filter(amount__gte=float(min_amount))

    if max_amount:
        deals = deals.filter(amount__lte=float(max_amount))

    if status:
        deals = deals.filter(status=status)

    if start_date:
        try:
            deals = deals.filter(created_at__date__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
        except ValueError:
            pass

    if end_date:
        try:
            deals = deals.filter(created_at__date__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
        except ValueError:
            pass

    # Сұрыптау
    if sort_by == "date_asc":
        deals = deals.order_by("created_at")
    elif sort_by == "date_desc":
        deals = deals.order_by("-created_at")
    elif sort_by == "amount_asc":
        deals = deals.order_by("amount")
    elif sort_by == "amount_desc":
        deals = deals.order_by("-amount")

    return render(request, 'crm/deal_list.html', {
        'deals': deals,
        'clients': clients,
        'filters': request.GET
    })



def home(request):
    return render(request, 'home.html')
@login_required
def create_deal(request):
    if not request.user.has_perm('crm.add_deal'):
        return HttpResponse("У вас нет прав доступа!", status=403)

    if request.method == 'POST':
        form = DealForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            deal = form.save()
            return redirect('deal_list')
    else:
        form = DealForm(user=request.user)

    return render(request, 'crm/create_deal.html', {'form': form})


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
