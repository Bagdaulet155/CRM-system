from django.shortcuts import render
from .models import Client
from django.http import HttpResponse

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'crm/client_list.html', {'clients': clients})

def home(request):
    return render(request, 'home.html') 