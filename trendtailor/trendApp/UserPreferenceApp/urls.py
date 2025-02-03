# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.preferences, name='set_preferences'),

]