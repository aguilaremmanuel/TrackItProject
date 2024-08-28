from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import User, Office

# Create your views here.
def user_login(request):
    return render(request, "user-login.html")

def generate_user_id(role_prefix):
    max_user_id = User.objects.filter(user_id__startswith=f"{role_prefix}-").aggregate(max_id=Max('user_id'))['max_id']
    if max_user_id:
        max_number = int(max_user_id.split('-')[1])
        new_number = max_number + 1
    else:
        new_number = 1000
    return f"{role_prefix}-{new_number:04d}"

#Hello world
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role_prefix = form.cleaned_data['role']
            user.user_id = generate_user_id(role_prefix)
            form.save()
            return redirect('user_login')  
    else:
        form = UserSignupForm()
    return render(request, "user-signup.html", {'form': form})

def system_admin_login(request):
    return render(request, "system_admin/system-admin-login.html")

def director_login(request):
    return render(request, "director-login.html")

def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")