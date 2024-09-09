from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import *
from django.utils import timezone
import random
import string
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# USER LOGIN
def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        
        # Fetch user by user_id
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('user_login')

        # Check user status
        if user.status == 'for verification':
            messages.error(request, "You are not verified yet.")
            return redirect('user_login')
        elif user.status == 'inactive':
            messages.error(request, "Your account is inactive. Please contact the administrator.")
            return redirect('user_login')
        elif user.status == 'archived':
            messages.error(request, "Your account has been archived and cannot be accessed.")
            return redirect('user_login')
        
        # Authenticate the user
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('user_login')
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
    if request.method == 'POST':
        form = SystemAdminLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            # Default credentials
            default_user_id = 'SYS-0001'
            default_password = 'SysAdmin@2024'
            
            # Check if the provided credentials match the default credentials
            if user_id == default_user_id and password == default_password:
                # You might want to create a dummy user or just proceed
                # For demonstration, we assume the user can log in successfully
                return redirect('system_admin_dashboard')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = SystemAdminLoginForm()
    
    return render(request, "system_admin/system-admin-login.html", {'form': form})

# SYSTEM ADMIN DASHBOARD
def system_admin_dashboard(request):
    return render(request, 'system_admin/system-admin-dashboard.html')

# SYSTEM ADMIN USER MANAGEMENT MODULE
def system_admin_user_management(request, office):
    if office == 'all-office':
        users = User.objects.exclude(status='archived')
    elif office == 'administrative':
        office_instance  = Office.objects.get(office_id='ADM')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived')
    elif office == 'accounting':
        office_instance  = Office.objects.get(office_id='ACC')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived')
    elif office == 'budgeting':
        office_instance  = Office.objects.get(office_id='BMD')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived')
    elif office == 'cashier':
        office_instance  = Office.objects.get(office_id='CSR')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived')
    elif office == 'payroll':
        office_instance  = Office.objects.get(office_id='PRL')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived')
    else:
        users = User.objects.none()

    return render(request, 'system_admin/system-admin-user-management.html', {'users': users, 'office': office})



# DIRECTOR LOGIN
def director_login(request):
    if request.method == 'POST':
        form = DirectorLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
    
            # Default credentials
            default_user_id = 'DIR-0001'
            default_password = 'Director@2024'
            
            # Check if the provided credentials match the default credentials
            if user_id == default_user_id and password == default_password:
                return redirect('dashboard_director')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = DirectorLoginForm()
    
    return render(request, "director-login.html", {'form': form})


# UPDATE USER STATUS
def update_user_status(request, user_id, action):
    try:
        user = User.objects.get(user_id=user_id)
        
        # Verify User
        if action == 'verify':
            user.status = 'active'
        
        # Reject User
        elif action == 'reject':
            user.status = 'inactive'
        
        # Deactivate User
        elif action == 'deactivate':
            user.status = 'inactive'
        
        # Archive User
        elif action == 'archive':
            user.status = 'archived'
        
        # Reactivate User
        elif action == 'reactivate':
            user.status = 'active'

        user.save()
        messages.success(request, f"User {action}d successfully!")
        
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    
    return redirect('system_admin_user_management', office='all-office')




# DIRECTOR DASHBOARD
def dashboard_director(request):
    return render(request, 'dashboard/director-dashboard.html')

# PASSWORD
def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")

# TEST COMMIT