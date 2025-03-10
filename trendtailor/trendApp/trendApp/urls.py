from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from trendApp import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('email-T1/', views.email_template_1, name='email_T1'),
    path('email-T2/', views.email_template_2, name='email_T2'),
    path('email-T3/', views.email_template_3, name='email_T3'),
    path('send-email/', views.send_email, name='send_email'), 
    path('', include('UserPreferenceApp.urls')),
    path('accounts/', include('accountsApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
