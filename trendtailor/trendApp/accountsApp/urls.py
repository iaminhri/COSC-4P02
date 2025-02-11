from django.urls import path
from .views import register, user_login

urlpatterns = [
    path('register/', register, name="register"),  # Maps to register.html
    path('login/', user_login, name="login"),      # Maps to login.html
]
