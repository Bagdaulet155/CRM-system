
from django.contrib import admin
from django.urls import path

from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', views.client_list, name='client_list'),
    path('', views.home, name='home'),
]
