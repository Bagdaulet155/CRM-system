from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView  # 👈 Добавь это
from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', views.client_list, name='client_list'),
    path('', views.home, name='home'),
    
    # Регистрация
    path('signup/', views.signup, name='signup'),
    
    # Вход
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # Выход 👇
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Сделки
    path('create_deal/', views.create_deal, name='create_deal'),
    path('deal_list/', views.deal_list, name='deal_list'),
]
