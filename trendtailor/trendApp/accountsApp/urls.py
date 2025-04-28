from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),  # Maps to register.html
    path('login/', views.user_login, name="login"),      # Maps to login.html
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name = 'profile'),
    path('edit/profile/', views.profile_form, name = 'edit_profile'),
    path('edit/profile/image', views.edit_profile_image, name = 'edit_image'),
    path('profile/settings', views.user_settings, name = 'settings'),
    path('logout/', views.auth_logout, name = 'logout'),

    path('schedule/', views.schedule_content, name='schedule_content'),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('edit-schedule/', views.edit_schedule, name='edit_schedule'),

    path('summarization/', views.summarization, name='summarization'),
]
