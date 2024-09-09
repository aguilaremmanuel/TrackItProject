from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('signup/',views.user_signup, name='user_signup'),
    path('admin-login/',views.system_admin_login, name='system_admin_login'),
    path('admin-dashboard/',views.system_admin_dashboard, name='system_admin_dashboard'),
    path('system-admin-user-management/<str:office>/', views.system_admin_user_management, name='system_admin_user_management'),
    
    path('director-login/',views.director_login, name='director_login'),
    path('director-dashboard/',views.dashboard_director, name='dashboard_director'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('new-password/',views.new_password, name='new_password'),
]
