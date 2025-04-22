from django.urls import path, include
from . import views
from rest_framework import routers
from UserPreferenceApp.views import ArticleViewSet, TypeViewSet

router = routers.SimpleRouter()
router.register('articles', ArticleViewSet, basename='articles')
router.register('type', TypeViewSet, basename='type')

urlpatterns = [
    path('preferences/', views.preferences, name='preferences'),
    path('user/contents/', views.user_contents, name='content_view'),
    path('news-api/', views.aggregate_content, name='news_api_view'),
    path('api/', include(router.urls)),
]
