from django.urls import path
from validacao import views

urlpatterns = [
    path('base/', views.base),
    path('add/', views.account, name='add_account'),    
    path('code/<int:account_id>/',  views.telegram, name='telegram_code'),
    path('success/', views.success, name='success_code_login'),
]