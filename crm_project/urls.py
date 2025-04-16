from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from crm import views

# Қате view-лерді өңдеу (handler404, handler500)
handler404 = 'crm.views.handler404'
handler500 = 'crm.views.handler500'

urlpatterns = [
    # Админ панелі
    path('admin/', admin.site.urls),

    # Басты бет
    path('', views.home, name='home'),

    # Аутентификация
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # қосымша
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Профиль
    path('profile/', views.profile_view, name='profile'),

    # Клиенттер
    path('clients/', views.client_list, name='client_list'),

    # Сделкалар
    path('create_deal/', views.create_deal, name='create_deal'),
    path('deal_list/', views.deal_list, name='deal_list'),

    # Избранное
    path('favorites/', views.favorite_deals, name='favorite_deals'),
    path('deals/<int:deal_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Отзывы
    path('client/<int:client_id>/review/', views.add_review, name='add_review'),
]
