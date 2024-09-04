from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, "user-login.html")

def user_signup(request):
    return render(request, "user-signup.html")

def system_admin_login(request):
    return render(request, "system_admin/system-admin-login.html")

def director_login(request):
    return render(request, "director-login.html")

def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")

def sidebar_header(request):
    return render(request, "sidebar-header.html")