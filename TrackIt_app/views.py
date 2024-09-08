from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import *
from django.utils import timezone

# USER LOGIN
def user_login(request):
    return render(request, "user-login.html")

# USER SIGNUP
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role_prefix = form.cleaned_data['role']
            user.user_id = generate_user_id(role_prefix)
            user.verified_date = timezone.now()
            form.save()
            return redirect('user_login')  
    else:
        form = UserSignupForm()
    return render(request, "user-signup.html", {'form': form})

# GENERATE USER ID
def generate_user_id(role_prefix):
    max_user_id = User.objects.filter(user_id__startswith=f"{role_prefix}-").aggregate(max_id=Max('user_id'))['max_id']
    if max_user_id:
        max_number = int(max_user_id.split('-')[1])
        new_number = max_number + 1
    else:
        new_number = 1000
    return f"{role_prefix}-{new_number:04d}"

# SYSTEM ADMIN LOGIN
def system_admin_login(request):
    return render(request, "system_admin/system-admin-login.html")

def system_admin_dashboard(request):
    return render(request, 'system_admin/system-admin-dashboard.html')

def system_admin_user_management(request):
    return render(request, 'system_admin/system-admin-user-management.html')

# DIRECTOR LOGIN
def director_login(request):
    return render(request, "director-login.html")

# PASSWORD
def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")