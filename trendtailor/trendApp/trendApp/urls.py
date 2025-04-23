from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('subscribe/', views.subscribeToChannel, name='subscribe'),

    path('email-T1/', views.email_template_1, name='email_T1'),
    path('email-T2/', views.email_template_2, name='email_T2'),
    path('email-T3/', views.email_template_3, name='email_T3'),
    path('email-T4/', views.email_template_4, name='email_T4'),
    path('email-T5/', views.email_template_5, name='email_T5'),

    path('', include('UserPreferenceApp.urls')),
    path('accounts/', include('accountsApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('share-email/<int:article_id>/<int:template_id>/', views.share_email, name='share_email'),  
    path("get-template-content/<int:article_id>/<int:template_id>/", views.get_template_content, name="get_template_content"),
    path("send-email/", views.send_email, name="send_email"),

    path('preview/', views.preview_content, name='preview_content'), # SNS Preview

    path("archived/", views.archived_contents, name="archived_contents"),
    path("archive/", views.archive_content, name="archive_content"),
    path("unarchive/<int:content_id>/", views.unarchive_content, name="unarchive_content"),
    path("export-archived-pdf/", views.export_archived_contents_pdf, name="export_archived_pdf"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
