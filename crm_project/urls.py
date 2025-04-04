from django.contrib import admin
from django.urls import path
from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', views.client_list, name='client_list'),
    path('', views.home, name='home'),
    
    # Добавляем URL для регистрации
    path('signup/', views.signup, name='signup'),
    
    # Добавляем URL для входа (используется CustomLoginView)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
    # Добавляем URL для создания сделки
    path('create_deal/', views.create_deal, name='create_deal'),
    
    # Добавляем URL для списка сделок
    path('deal_list/', views.deal_list, name='deal_list'),
]
