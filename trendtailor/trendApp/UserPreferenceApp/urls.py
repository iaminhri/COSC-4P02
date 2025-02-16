# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.preferences, name='preferences'),
    path('user/contents/', views.user_contents, name='content_view'),
    path('news-api/', views.aggregate_content, name='news_api_view'),
]