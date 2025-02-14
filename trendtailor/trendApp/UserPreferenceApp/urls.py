# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.preferences, name='set_preferences'),
    path('news-api/', views.aggregate_content, name='news_api_view'),
]