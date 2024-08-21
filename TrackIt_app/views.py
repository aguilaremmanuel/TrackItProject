from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, "user_login.html")

def user_signup(request):
    return render(request, "user_signup.html")

def sysAdLogin(request):
    return render(request, "system_admin/sysAdLogin.html")

