from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import *
from django.utils import timezone
import random
import string
#from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


# USER LOGIN
def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']

        # Fetch user by user_id and password (plain-text password comparison)
        try:
            user = User.objects.get(user_id=user_id, password=password)  # Directly comparing passwords
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect('user_login')

        # Check user status
        if user.status == 'for verification':
            messages.error(request, "Your account is pending for verification. Please wait for approval.")
            return redirect('user_login')
        elif user.status == 'inactive':
            messages.error(request, "Your account is inactive. Please contact the administrator to reactivate.")
            return redirect('user_login')
        elif user.status == 'archived':
            messages.error(request, "Your account has been deleted and cannot be accessed.")
            return redirect('user_login')

        # Manually log the user in by setting the session
        request.session['user_id'] = user.user_id

        # Redirect based on user role
        if user.role == 'ADO':  # Admin Officer
            return redirect('dashboard_admin_officer')
        elif user.role == 'SRO':  # Sub-Receiving Officer
            return redirect('dashboard_sro')
        elif user.role == 'ACT':  # Action Officer
            return redirect('dashboard_action_officer')
        else:
            # In case the role is not recognized
            messages.error(request, "Invalid role. Please contact the administrator.")
            return redirect('user_login')

    return render(request, "user-login.html")


#USER UPDATE STATUS AND EMAILING FUNCTION
def update_user_status(request, user_id, action, office):
    user = User.objects.get(pk=user_id)  # Fetch the user object

    if action == 'verify':
        user.status = 'active'
        subject = 'Your Account Has Been Verified'
        # Include user_id and password in the message
        message = (
            f"Hello {user.firstname},\n\n"
            f"Your account has been verified and is now active.\n\n"
            f"Your User ID: {user.user_id}\n"
            f"Your Password: {user.password}  \n\n"
            "Please keep this information secure.\n\n"
            "Regards,\n"
            "TrackIt Team"
        )
    elif action == 'reject':
        user.status = 'rejected'
        subject = 'Your Account Has Been Rejected'
        message = 'Your account has been rejected. Please contact support for more information.'
    elif action == 'deactivate':
        user.status = 'inactive'
        subject = 'Your Account Has Been Deactivated'
        message = 'Your account has been deactivated. Please contact support to reactivate it.'
    elif action == 'archive':
        user.status = 'archived'
        subject = 'Your Account Has Been Archived'
        message = 'Your account has been archived. You will not be able to log in.'
    elif action == 'reactivate':
        user.status = 'active'
        subject = 'Your Account Has Been Reactivated'
        message = 'Your account has been reactivated and is now active.'
    else:
        return HttpResponse("Invalid action", status=400)

    user.save()  # Save the updated status

    if action != 'archive':
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    return redirect('system_admin_user_management', office=office)


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

            # Get user email
            user_email = form.cleaned_data['email']

            # Send an email notifying the user of their status
            send_mail(
                subject='TrackIt: Account Status',
                message=f"Hello {user.firstname},\n\nThank you for signing up! Your account is currently '{user.status}'. We will notify you when it is verified.\n\nRegards,\nTrackIt Team",
                from_email=settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in your settings
                recipient_list=[user_email],
                fail_silently=False,
            )

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


    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if sort_by in ['role', 'status', 'lastname', 'email']:  # Only allow sorting by valid fields
        if order == 'asc':
            users = users.order_by(sort_by)
        else:
            users = users.order_by(f'-{sort_by}')

    return render(request, 'system_admin/system-admin-user-management.html', {'users': users, 'office': office})

# SYSTEM ADMIN DOC MANAGEMENT
def system_admin_doc_management(request):
    return render(request, 'system_admin/system-admin-doc-management.html')

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


# DIRECTOR DASHBOARD
def dashboard_director(request):
    return render(request, 'director/director-dashboard.html')

# SRO DASHBOARD
def dashboard_sro(request):
    return render(request, 'sro/sro-dashboard.html')

# ADMIN OFFICER DASHBOARD
def dashboard_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-dashboard.html')

# ADMIN OFFICER NEW RECORD
def new_record_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-new-record.html')

# ADMIN OFFICER ALL RECORDS
def all_records_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-all-records.html')

# ADMIN OFFICER NEEDS ACTION
def needs_action_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-needs-action.html')

# ADMIN OFFICER OVERDUE
def overdue_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-overdue.html')

# ADMIN OFFICER ARCHIVE
def archive_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-archive.html')

# ADMIN OFFICER ACTIVITY LOGS
def activity_logs_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-activity-logs.html')

# ACTION OFFICER DASHBOARD
def dashboard_action_officer(request):
    return render(request, 'action_officer/action-officer-dashboard.html')

# PASSWORD
def forgot_password(request):
    return render(request, "forgot-password.html")

def new_password(request):
    return render(request, "new-password.html")

# TEST COMMIT