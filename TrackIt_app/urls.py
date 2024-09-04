from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('signup/',views.user_signup, name='user_signup'),
    path('admin-login/',views.system_admin_login, name='system_admin_login'),
    path('director-login/',views.director_login, name='director_login'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('new-password/',views.new_password, name='new_password'),
    path('sidebar-header/',views.sidebar_header, name='sidebar_header'),
]
