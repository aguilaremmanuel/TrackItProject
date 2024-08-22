from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, "user-login.html")

def user_signup(request):
    return render(request, "user-signup.html")

def system_admin_login(request):
    return render(request, "system_admin/system-admin-login.html")

