from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),  # Maps to register.html
    path('login/', views.user_login, name="login"),      # Maps to login.html
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name = 'profile'),
    path('logout/', views.auth_logout, name = 'logout'),
]
