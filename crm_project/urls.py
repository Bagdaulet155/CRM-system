from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from crm import views  # crm қосымшасын импорттау
print(dir(views))  # 👈 бұл views ішінде не бар екенін көрсетеді

urlpatterns = [
    # Админ панелі
    path('admin/', admin.site.urls),

    # Клиенттер
    path('clients/', views.client_list, name='client_list'),

    # Басты бет
    path('', views.home, name='home'),

    # Тіркелу
    path('signup/', views.signup, name='signup'),

    # Кіру (екі түрлі жолмен)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # Қосымша жол

    # Шығу
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Сделки (мәмілелер)
    path('create_deal/', views.create_deal, name='create_deal'),
    path('deal_list/', views.deal_list, name='deal_list'),
]

# Қателерді өңдеу
handler404 = 'crm.views.handler404'
handler500 = 'crm.views.handler500'
