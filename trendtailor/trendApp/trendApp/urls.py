from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('email-T1/', views.email_template_1, name='email_T1'),  # Email template 1 page
    path('email-T2/', views.email_template_2, name='email_T2'),  # Email template 2 page
    path('email-T3/', views.email_template_3, name='email_T3'),  # Email template 3 page
    # path('email-T4/', views.email_template_4, name='email_T4'),  # Email template 4 page
    # path('email-T5/', views.email_template_5, name='email_T5'),  # Email template 5 page
    path('', include('UserPreferenceApp.urls')),
    path('accounts/', include('accountsApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('share-email/<int:article_id>/<int:template_id>/', views.share_email, name='share_email'), # share email
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
