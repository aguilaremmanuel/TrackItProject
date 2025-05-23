from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import qrcode, pytz, json
from io import BytesIO
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils.timezone import now
from datetime import datetime, timedelta, date, time
from xhtml2pdf import pisa
import os, shutil
from django.shortcuts import get_object_or_404
from django.db.models import Count
from itertools import chain
from django.db.models import F
from django.db.models import Value
from dateutil.relativedelta import relativedelta
from django.db.models import Case, When, Value, IntegerField
from django.utils.timezone import make_aware


#---------------
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import random
# ----------- LOGIN AND SIGNUP -----------------

#-------- STYLES FOR USER UPDATE ------------
# Define a common CSS style
common_style = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
        line-height: 1.6;
        color: #333;
    }
    .email-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: 50px auto;
        overflow: hidden;
    }
    .email-header {
        background-color: #007BFF;
        padding: 15px;
        text-align: center;
        color: #fff;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
    }
    .email-content {
        padding: 30px;
        font-size: 16px;
        color: #555;
    }
    .email-content p {
        margin: 0 0 20px;
    }
    .email-content h1 {
        font-size: 22px;
        margin-bottom: 10px;
        color: #007BFF;
    }
    .email-content a.button {
        display: inline-block;
        padding: 12px 25px;
        font-size: 16px;
        background-color: #28a745;
        color: white;
        border-radius: 5px;
        text-decoration: none;
        margin-top: 20px;
    }
    .email-footer {
        text-align: center;
        padding: 20px;
        background-color: #f8f9fa;
        border-top: 1px solid #dddddd;
        font-size: 14px;
        color: #777777;
    }
    .email-footer p {
        margin: 0;
    }
    .email-container .logo {
        width: 120px;
        margin: 0 auto;
    }
</style>
"""

# USER SIGNUP
def user_signup(request):

    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():

            user_email = form.cleaned_data['email']
            if User.objects.filter(email=user_email).exists():
                form.add_error('email', "A user with this email already exists.")
                return render(request, "user-signup.html", {'form': form})

            employee_id = form.cleaned_data['employee_id']
            if User.objects.filter(employee_id=employee_id).exists():
                form.add_error('employee_id', "A user with this Employee ID already exists.")
                return render(request, "user-signup.html", {'form': form})

            try:
                user = form.save(commit=False)
                role_prefix = form.cleaned_data['role']
                user.user_id = generate_user_id(role_prefix)
                user.registered_date = timezone.now()
                user.save()

                # Get user email
                user_email = form.cleaned_data['email']

                # Define subject and message content
                subject = 'TrackIt: Account Status'

                # HTML message with advanced styling
                html_message = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            line-height: 1.6;
                            color: #333;
                        }}
                        .email-container {{
                            background-color: #ffffff;
                            padding: 30px;
                            border-radius: 10px;
                            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                            max-width: 600px;
                            margin: 50px auto;
                            overflow: hidden;
                        }}
                        .email-header {{
                            background-color: #007BFF;
                            padding: 20px;
                            text-align: center;
                            color: #fff;
                            font-size: 24px;
                            font-weight: bold;
                            border-radius: 10px 10px 0 0;
                        }}
                        .email-content {{
                            padding: 30px;
                            font-size: 16px;
                            color: #555;
                        }}
                        .email-content p {{
                            margin: 0 0 20px;
                        }}
                        .email-content h1 {{
                            font-size: 22px;
                            margin-bottom: 10px;
                            color: #007BFF;
                        }}
                        .email-content a.button {{
                            display: inline-block;
                            padding: 12px 25px;
                            font-size: 16px;
                            background-color: #28a745;
                            color: white;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }}
                        .email-footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            border-top: 1px solid #dddddd;
                            font-size: 14px;
                            color: #777777;
                        }}
                        .email-footer p {{
                            margin: 0;
                        }}
                        .email-container .logo {{
                            width: 120px;
                            margin: 0 auto;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <!-- Email Header -->
                        <div class="email-header">
                            <h1>TrackIt: Account Status</h1>
                        </div>
                        
                        <div class="email-content">
                            <h1>Hello {user.firstname},</h1>
                            <p>Thank you for signing up for TrackIt! We're excited to have you on board.</p>
                            <p>Your account is currently <strong>{user.status}</strong>. We will notify you as soon as it is verified.</p>
                            <p>In the meantime, if you have any questions, don't hesitate to reach out to our support team.</p>
                        </div>

                        <!-- Email Footer -->
                        <div class="email-footer">
                            <p>Regards,<br><strong>TrackIt Team</strong></p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Plain text fallback
                plain_message = strip_tags(html_message)

                # Create and send the email
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)

                return redirect('user_login')
            except IntegrityError:
                form.add_error('email', "A user with this email already exists.")
    else:
        form = UserSignupForm()

    return render(request, "user-signup.html", {'form': form})


    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():

            user_email = form.cleaned_data['email']
            if User.objects.filter(email=user_email).exists():
                form.add_error('email', "A user with this email already exists.")
                return render(request, "user-signup.html", {'form': form})

            employee_id = form.cleaned_data['employee_id']
            if User.objects.filter(employee_id=employee_id).exists():
                form.add_error('employee_id', "A user with this Employee ID already exists.")
                return render(request, "user-signup.html", {'form': form})

            try:
                user = form.save(commit=False)
                role_prefix = form.cleaned_data['role']
                user.user_id = generate_user_id(role_prefix)
                user.registered_date = timezone.now()
                user.save()

                # Get user email
                user_email = form.cleaned_data['email']

                # Define subject and message content
                subject = 'TrackIt: Account Status'

                # HTML message with advanced styling
                html_message = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            line-height: 1.6;
                            color: #333;
                        }}
                        .email-container {{
                            background-color: #ffffff;
                            padding: 30px;
                            border-radius: 10px;
                            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                            max-width: 600px;
                            margin: 50px auto;
                            overflow: hidden;
                        }}
                        .email-header {{
                            background-color: #007BFF;
                            padding: 20px;
                            text-align: center;
                            color: #fff;
                            font-size: 24px;
                            font-weight: bold;
                            border-radius: 10px 10px 0 0;
                        }}
                        .email-content {{
                            padding: 30px;
                            font-size: 16px;
                            color: #555;
                        }}
                        .email-content p {{
                            margin: 0 0 20px;
                        }}
                        .email-content h1 {{
                            font-size: 22px;
                            margin-bottom: 10px;
                            color: #007BFF;
                        }}
                        .email-content a.button {{
                            display: inline-block;
                            padding: 12px 25px;
                            font-size: 16px;
                            background-color: #28a745;
                            color: white;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }}
                        .email-footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            border-top: 1px solid #dddddd;
                            font-size: 14px;
                            color: #777777;
                        }}
                        .email-footer p {{
                            margin: 0;
                        }}
                        .email-container .logo {{
                            width: 120px;
                            margin: 0 auto;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <!-- Email Header -->
                        <div class="email-header">
                            <h1>TrackIt: Account Status</h1>
                        </div>
                        
                        <div class="email-content">
                            <h1>Hello {user.firstname},</h1>
                            <p>Thank you for signing up for TrackIt! We're excited to have you on board.</p>
                            <p>Your account is currently <strong>{user.status}</strong>. We will notify you as soon as it is verified.</p>
                            <p>In the meantime, if you have any questions, don't hesitate to reach out to our support team.</p>
                        </div>

                        <!-- Email Footer -->
                        <div class="email-footer">
                            <p>Regards,<br><strong>TrackIt Team</strong></p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Plain text fallback
                plain_message = strip_tags(html_message)

                # Create and send the email
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)

                return redirect('user_login')
            except IntegrityError:
                form.add_error('email', "A user with this email already exists.")
    else:
        form = UserSignupForm()

    return render(request, "user-signup.html", {'form': form})

# -------------- 2FA -------------------
@csrf_exempt
def toggle_two_factor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        two_factor_enabled = data.get('two_factor_enabled', False)

        # Get the logged-in user
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=403)

        try:
            user = User.objects.get(user_id=user_id)
            user.two_factor_enabled = two_factor_enabled

            # Clear the 2FA code if 2FA is turned off
            if not two_factor_enabled:
                user.two_factor_code = None

            user.save()
            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#3start
FAILED_LOGIN_THRESHOLD = 3
TEMP_BAN_TIME = 30  

def user_login(request):
    if request.method == 'POST':
        # 1. Check if we are in the 2FA verification step
        if 'two_factor_code' in request.POST:
            # Handle 2FA code verification
            return handle_two_factor_verification(request)

        # 2. Otherwise, handle initial login attempt
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)

        # Remember Me logic: Save credentials in session
        if remember_me:
            request.session['remember_me'] = True
            request.session['remembered_user_id'] = user_id
            request.session['remembered_password'] = password
        else:
            # Clear remembered credentials if "Remember Me" is not checked
            request.session.pop('remember_me', None)
            request.session.pop('remembered_user_id', None)
            request.session.pop('remembered_password', None)
        
        if remember_me:
            request.session['remember_me'] = True
        else:
            request.session.pop('remember_me', None)

        # Ensure both user_id and password are provided
        if not user_id or not password:
            messages.error(request, "Please enter both User ID and Password.")
            return redirect('user_login')

        # Retrieve or initialize login attempts data from session
        login_attempts = request.session.get('login_attempts', {})
        user_attempts = login_attempts.get(user_id, {'count': 0, 'banned_until': None})

        # Convert `banned_until` from string to `datetime` if it exists
        if user_attempts['banned_until']:
            user_attempts['banned_until'] = datetime.fromisoformat(user_attempts['banned_until'])

        # Check if the user is temporarily banned
        if user_attempts['banned_until'] and now() < user_attempts['banned_until']:
            ban_time_left = (user_attempts['banned_until'] - now()).seconds
            return render(request, 'user-login.html', {
                'ban_time_left': ban_time_left,
                'remembered_user_id': user_id,
                'remembered_password': password,
                'remember_me_checked': remember_me
            })

        # Authenticate the user
        try:
            user = User.objects.get(user_id=user_id, password=password)
        except User.DoesNotExist:
            # Increment failed login attempts
            user_attempts['count'] += 1
            if user_attempts['count'] >= FAILED_LOGIN_THRESHOLD:
                # Temporarily ban the user
                ban_until = now() + timedelta(seconds=TEMP_BAN_TIME)
                user_attempts['banned_until'] = ban_until.isoformat()  # Serialize datetime
                login_attempts[user_id] = user_attempts
                request.session['login_attempts'] = login_attempts  # Save to session
                return render(request, 'user-login.html', {
                    'ban_time_left': TEMP_BAN_TIME,
                    'remembered_user_id': user_id,
                    'remembered_password': password,
                    'remember_me_checked': remember_me
                })
            else:
                remaining_attempts = FAILED_LOGIN_THRESHOLD - user_attempts['count']
                messages.error(request, f"Invalid credentials. You have {remaining_attempts} attempt(s) left.")
                login_attempts[user_id] = user_attempts
                request.session['login_attempts'] = login_attempts  # Save to session
                return redirect('user_login')

        # Reset login attempts after successful login
        if user_id in login_attempts:
            del login_attempts[user_id]
            request.session['login_attempts'] = login_attempts

        # Check if the user's status prevents them from logging in and specify the error message
        if user.status == 'for verification':
            messages.error(request, "Your account is still under verification. Please wait for approval.")
            return redirect('user_login')
        elif user.status == 'inactive':
            messages.error(request, "Your account is inactive. Please contact support for assistance.")
            return redirect('user_login')
        elif user.status == 'rejected':
            messages.error(request, "Your account has been rejected. You cannot log in at this time.")
            return redirect('user_login')
        elif user.status == 'archived':
            messages.error(request, "Your account is archived. Please contact the administrator for more information.")
            return redirect('user_login')
        
        # Check if 2FA is enabled
        if user.two_factor_enabled:
            # Generate a 6-digit 2FA code, save it, and send it by email
            two_factor_code = f"{random.randint(100000, 999999)}"
            user.two_factor_code = two_factor_code
            user.save()

            send_mail(
                'Your 2FA Code',
                f'Your Two-Factor Authentication code is: {two_factor_code}',
                'no-reply@example.com',
                [user.email]
            )

            # Temporarily store the user ID in session for 2FA verification
            request.session['temp_user_id'] = user.user_id
            # Render the page for the 2FA code entry
            # return render(request, 'user-login.html', {'two_factor_step': True})
            return render(request, 'user-login.html', {'two_factor_step': True, 'request': request})    
        
        # Handle "Remember Me" functionality
        if remember_me:
            request.session.set_expiry(timedelta(days=30)) 
        else:
            request.session.set_expiry(0) 

        # If 2FA is not enabled, proceed with login
        user.last_login = timezone.now()
        user.save()
        set_user_session(request, user)
        return redirect_user_dashboard(user.role)

    # Pre-fill form if "Remember Me" was previously checked
    remembered_user_id = request.session.get('remembered_user_id', '')
    remembered_password = request.session.get('remembered_password', '')
    remember_me_checked = request.session.get('remember_me', False)

    return render(request, 'user-login.html', {
        'ban_time_left': 0,
        'remembered_user_id': remembered_user_id,
        'remembered_password': remembered_password,
        'remember_me_checked': remember_me_checked,
    })

def handle_two_factor_verification(request):
    """Separate function to handle the 2FA code verification step."""
    temp_user_id = request.session.get('temp_user_id')
    two_factor_code = request.POST.get('two_factor_code')

    # Retrieve the user using temp_user_id and verify the 2FA code
    try:
        user = User.objects.get(user_id=temp_user_id, two_factor_code=two_factor_code)
    except User.DoesNotExist:
        messages.error(request, "Invalid 2FA code.")
        return render(request, 'user-login.html', {'two_factor_step': True})

    # Clear the 2FA code after successful verification
    user.two_factor_code = None
    user.last_login = timezone.now()
    user.save()
    set_user_session(request, user)

    # Redirect to the appropriate dashboard
    return redirect_user_dashboard(user.role)

def set_user_session(request, user):
    # Helper to set session and user profile
    role_map = {
        'ADO': 'Admin Officer',
        'SRO': 'Sub-receiving Officer',
        'ACT': 'Action Officer',
        'Director': 'Director',
        'System Admin': 'System Administrator'
    }
    role = role_map.get(user.role, 'Unknown')
    middlename = user.middlename.title() if user.middlename else ''

    user_profile = {
        'user_id': user.user_id,
        'role': role,
        'firstname': user.firstname.title(),
        'middlename': middlename,
        'lastname': user.lastname.title(),
        'email': user.email,
        'contact_no': user.contact_no,
        'profile_picture': user.profile_picture.name,
        'two_factor_enabled': user.two_factor_enabled
    }

    request.session['user_profile'] = user_profile
    request.session['user_id'] = user.user_id

def redirect_user_dashboard(role):
    # Redirects user based on role
    dashboard_map = {
        'ADO': 'admin_officer_dashboard',
        'SRO': 'sro_dashboard',
        'ACT': 'action_officer_dashboard',
        'Director': 'director_dashboard',
        'System Admin': 'system_admin_dashboard'
    }
    return redirect(f"{reverse(dashboard_map.get(role))}?status=active")

# USER LOGOUT
def user_logout(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if user_id:
        del request.session['user_id']
        del request.session['user_profile']
    
    if role == 'DIR':
        return redirect(user_login)
    elif role == 'SYS':
        return redirect(user_login)

    return redirect(user_login)

# -------------- DASHBOARD -------------------

def system_admin_dashboard(request):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    return render(request, 'system_admin/system-admin-dashboard.html', {
        'user_profile': user_profile
    })

# DIRECTOR DASHBOARD
def director_dashboard(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)
    
    announcements = Announcement.objects.filter(
        Q(all_offices=True) | Q(offices__icontains='Director')
    )

    records = Document.objects.filter(status='For DIR Approval')

    context = {
        'announcements': announcements,
        'user_profile': user_profile,
        'records': records,
    }

    return render(request, 'director/director-dashboard.html', context)

# ADMIN OFFICER DASHBOARD
def admin_officer_dashboard(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    # Fetch the announcements based on either condition
    announcements = Announcement.objects.filter(
        Q(all_offices=True) | Q(offices__icontains='Admin')
    )

    context = {
        'user_profile': user_profile,
        'announcements': announcements,  # Add announcements to context
    }

    return render(request, 'admin_officer/admin-officer-dashboard.html', context)

# SRO DASHBOARD
def sro_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    # Fetch the user's information from the database
    user = User.objects.filter(user_id=user_id).first()
    
    office_name = user.office_id.office_name

    # Fetch the announcements based on either condition
    announcements = Announcement.objects.filter(
        Q(all_offices=True) | Q(offices__icontains=office_name)
    )

    context = {
        'user_profile': user_profile,
        'announcements': announcements
    }

    return render(request, 'sro/sro-dashboard.html', context)

# ACTION OFFICER DASHBOARD
def action_officer_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    user = User.objects.filter(user_id=user_id).first()
    
    office_name = user.office_id.office_name

    # Fetch the announcements based on either condition
    announcements = Announcement.objects.filter(
        Q(all_offices=True) | Q(offices__icontains=office_name)
    )

    context = {
        'user_profile': user_profile,
        'announcements': announcements
    }

    return render(request, 'action_officer/action-officer-dashboard.html', context)

# -------------- USER MANAGEMENT -------------------

# SYSTEM ADMIN USER MANAGEMENT MODULE
def system_admin_user_management(request, office):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    context = {
        'office': office,
        'user_profile': user_profile
    }

    # Render the system admin user management page
    return render(request, 'system_admin/system-admin-user-management.html', context)


# DIRECTOR USER MANAGEMENT MODULE
def director_user_management(request, office):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile,
        'office': office,
    }

    return render(request, 'director/director-user-management.html', context)

# -------------- DOC MANAGEMENT -------------------

# SYSTEM ADMIN DOC MANAGEMENT
def system_admin_doc_management(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    if request.method == 'POST':
        
        document_type = request.POST.get('document_type')
        category = request.POST.get('category')
        priority_level_str = request.POST.get('priority_level')
        route_list = request.POST.getlist('route[]')
        
        priority_level = PriorityLevel.objects.get(priority_level=priority_level_str)

        new_document_type = DocumentType.objects.create(
            document_type=document_type,
            category=category,
            priority_level=priority_level,
            last_update=timezone.now()
        )

        for route in route_list:
            office = Office.objects.get(office_name=route)  # Fetch the Office instance
            DocumentRoute.objects.create(
                document_type=new_document_type,
                route=office
            )

        DocumentManagementLogs.objects.create(
            time_stamp = timezone.now(),
            document_type=new_document_type,
            activity='Document Type Created',
            user_id=user_id
        )

    context = {
        'user_profile': user_profile
    }

    return render(request, 'system_admin/system-admin-doc-management.html', context)

# SYSTEM ADMIN DOC MANAGEMENT
def director_doc_management(request):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    if request.method == 'POST':
        document_type = request.POST.get('document_type')
        category = request.POST.get('category')
        priority_level_str = request.POST.get('priority_level')
        route_list = request.POST.getlist('route[]')
        
        priority_level = PriorityLevel.objects.get(priority_level=priority_level_str)

        new_document_type = DocumentType.objects.create(
            document_type=document_type,
            category=category,
            priority_level=priority_level,
            last_update=timezone.now()
        )

        for route in route_list:
            office = Office.objects.get(office_name=route)
            DocumentRoute.objects.create(
                document_type=new_document_type,
                route=office
            )

        DocumentManagementLogs.objects.create(
            time_stamp=timezone.now(),
            document_type=new_document_type,
            activity='Document Type Created',
            user_id=user_id
        )

    context = {
        'user_profile': user_profile
    }

    return render(request, 'director/director-doc-management.html', context)

# -------------- NEW RECORD -------------------

# SYSTEM ADMIN OFFICER NEW RECORD
def system_admin_new_record(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    re_upload = request.GET.get('reupload')

    if re_upload:
        document = Document.objects.get(document_no=re_upload)
        return render(request, 'system_admin/system-admin-new-record.html', {
            'user_profile': user_profile,
            'document': document
        })

    return render(request, 'system_admin/system-admin-new-record.html', {
        'user_profile': user_profile
    })

# ADMIN OFFICER NEW RECORD
def admin_officer_new_record(request):

    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    re_upload = request.GET.get('reupload')

    if re_upload:
        document = Document.objects.get(document_no=re_upload)
        return render(request, 'admin_officer/admin-officer-new-record.html', {
            'user_profile': user_profile,
            'document': document
        })

    return render(request, 'admin_officer/admin-officer-new-record.html', {
        'user_profile': user_profile,
    })

COUNTER_FILE = os.path.join(os.path.dirname(__file__), 'counter.txt')

# Function to read the last tracking number from the file
def get_last_tracking_number():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as file:
            return file.read().strip()
    return None

# Function to generate a new tracking number
def generate_tracking_number():
    current_year = str(timezone.now().year)[-2:]  # Get last two digits of the year
    last_number = 0
    last_tracking_number = get_last_tracking_number()

    if last_tracking_number and last_tracking_number.startswith(f"FO-{current_year}-"):
        last_number = int(last_tracking_number.split('-')[-1])

    new_tracking_number = f"FO-{current_year}-{last_number + 1:04d}"
    return new_tracking_number


# API endpoint to handle tracking number generation
def generate_tracking_number_api(request):
    if 'uncommitted_tracking_no' not in request.session:
        request.session['uncommitted_tracking_no'] = generate_tracking_number()
    return JsonResponse({"tracking_no": request.session['uncommitted_tracking_no']})

def add_record(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':
        # Extract data from POST request
        tracking_no = request.POST.get('tracking_no')
        sender_name = request.POST.get('sender_name')
        sender_dept = request.POST.get('sender_dept')
        doc_type = request.POST.get('doc_type')
        subject = request.POST.get('subject')
        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')

         # Validation: Reject manually entered "FO" Tracking Numbers
        if tracking_no.startswith("FO") and 'uncommitted_tracking_no' not in request.session:
            messages.error(
                request,
                "Invalid Tracking Number. If the document has no Tracking Number, you can generate one by clicking the TN Generator."
            )
            return render(request, 'your_template.html', {"error": "Invalid Tracking Number."})

        # Simulate saving the document
        print(f"Saving document: TN={tracking_no}, Sender={sender_name}, Remarks={remarks}")

       # Save only auto-generated Tracking Numbers to counter.txt
        if 'uncommitted_tracking_no' in request.session and tracking_no == request.session['uncommitted_tracking_no']:
            with open(COUNTER_FILE, 'w') as file:
                file.write(tracking_no)
            del request.session['uncommitted_tracking_no']  # Remove uncommitted TN

        try:
            document = Document.objects.get(tracking_no=tracking_no)

            if document.is_rejected:

                document.sender_name = sender_name
                document.status = 'For DIR Approval'
                document.sender_department = sender_dept
                document.document_type_id = doc_type
                document.subject = subject
                document.remarks = remarks
                document.is_rejected = False
                document.save()

                new_remarks = Remarks.objects.create(
                    remarks=remarks
                )

                if file_attachment:
                    folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(document.document_no))
                    file_attachment = handle_file_versioning(file_attachment, folder_path)

                ActivityLogs.objects.create(
                    time_stamp=timezone.now(),
                    activity='Document Reupload',
                    document_id=document,
                    user_id_id=user_id,
                    remarks = new_remarks,
                    file_attachment = file_attachment
                )

                routes = DocumentRoute.objects.filter(document_type=document.document_type)
        
                str_routes, str_routes_titles = generate_route_strings(routes)
                qr_code_url = request.build_absolute_uri(f'/generate-qrcode/{document.document_no}/')
                str_tracking_no = tracking_no
                document_no = document.document_no

                data = {
                    'str_routes': str_routes,
                    'str_routes_titles': str_routes_titles,
                    'qr_code_url': qr_code_url,
                    'str_tracking_no': str_tracking_no,
                    'document_no': document_no,
                    'recordExists': False
                }
                
                # Return a JSON response indicating success
                return JsonResponse(data)

            else: 

                data = {
                    'trackingNo': tracking_no,
                    'recordExists': True
                }

                return JsonResponse(data)

        except Document.DoesNotExist:

            document = create_document(tracking_no, sender_name, sender_dept, doc_type, subject, remarks, file_attachment, user_id)

            routes = DocumentRoute.objects.filter(document_type=document.document_type)
            
            str_routes, str_routes_titles = generate_route_strings(routes)
            qr_code_url = request.build_absolute_uri(f'/generate-qrcode/{document.document_no}/')
            str_tracking_no = tracking_no
            document_no = document.document_no

            data = {
                'str_routes': str_routes,
                'str_routes_titles': str_routes_titles,
                'qr_code_url': qr_code_url,
                'str_tracking_no': str_tracking_no,
                'document_no': document_no,
                'recordExists': False
            }
            
            return JsonResponse(data)
    
    if role == 'ADO':
        return redirect(admin_officer_new_record)
    elif role == 'SYS':
        return redirect(system_admin_new_record)

# ---------------- ALL RECORDS -------------------

# SYSTEM ADMIN ALL RECORDS
def system_admin_all_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    return render(request, 'system_admin/system-admin-all-records.html', {
        'user_profile': user_profile,
    })

# ADMIN OFFICER ALL RECORDS
def admin_officer_all_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    return render(request, 'admin_officer/admin-officer-all-records.html', {'user_profile': user_profile})

# DIRECTOR ALL RECORDS
def director_all_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role, id = user_id.split('-')
    if role != 'DIR':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']
    
    context = {
        'user_profile': user_profile,
    }

    if id == '1002':

        return render(request, 'director/director-plus-all-records.html', context)

    return render(request, 'director/director-all-records.html', context)

# ----------------- RECORDS -------------------

# SRO RECORDS
def sro_records(request, panel, scanned_document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    selected_documents = request.session.get('selected_documents')

    if selected_documents:
        del request.session['selected_documents']

    if int(scanned_document_no) < 0:
        return render(request, 'sro/sro-records.html', {'panel': panel, 'user_profile': user_profile})
    
    user = User.objects.get(user_id=user_id)
    office = user.office_id_id

    try:
        document = Document.objects.get(document_no=scanned_document_no)
    except Document.DoesNotExist:
        scanned_status = "not-found"

        context = {
            'user_profile': user_profile,
            'panel': panel,
            'scanned_status': scanned_status,
        }

        return render(request, 'sro/sro-records.html', context)

    if document.status in ["For SRO Receiving", "For Resolving"] and document.next_route == office:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_name': user_profile,
        'role': role,
        'panel': panel,
        'scanned_document_no': scanned_document_no,
        'scanned_status': scanned_status,
        'document_details': get_document_details(document)
    }

    return render(request, 'sro/sro-records.html', context)

# ACTION OFFICER RECORDS
def action_officer_records(request, scanned_document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    selected_documents = request.session.get('selected_documents')

    if selected_documents:
        del request.session['selected_documents']

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    if int(scanned_document_no) < 0:
        return render(request, 'action_officer/action-officer-records.html', {'user_profile': user_profile})

    user = User.objects.get(user_id=user_id)

    try:
        document = Document.objects.get(document_no=scanned_document_no)
    except Document.DoesNotExist:
        scanned_status = "not-found"

        context = {
            'user_profile': user_profile,
            'scanned_status': scanned_status,
        }

        return render(request, 'action_officer/action-officer-records.html', context)

    if document.status == 'For ACT Receiving' and document.next_route == user.office_id_id and document.act_receiver == user_id:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_profile': user_profile,
        'role': role,
        'scanned_document_no': scanned_document_no,
        'scanned_status': scanned_status,
        'document_details': get_document_details(document)
    }

    return render(request, 'action_officer/action-officer-records.html', context)

# ---------------- NEEDS ACTION -------------------

# ADMIN OFFICER NEEDS ACTION
def admin_officer_needs_action(request, panel, scanned_document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    selected_documents = request.session.get('selected_documents')
    if selected_documents:
        del request.session['selected_documents']
    
    if int(scanned_document_no) < 0:
        return render(request, 'admin_officer/admin-officer-needs-action.html', {
            'panel': panel,
            'user_profile': user_profile
        })

    try:
        document = Document.objects.get(document_no=scanned_document_no)
    except Document.DoesNotExist:
        scanned_status = "not-found"

        context = {
            'user_profile': user_profile,
            'panel': panel,
            'scanned_status': scanned_status,
        }

        return render(request, 'admin_officer/admin-officer-needs-action.html', context)

    if document.status in ["For Routing", "For Archiving", "Rejected"]:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_profile': user_profile,
        'role': role,
        'panel': panel,
        'scanned_document_no': scanned_document_no,
        'scanned_status': scanned_status,
        'document_details': get_document_details(document)
    }

    return render(request, 'admin_officer/admin-officer-needs-action.html', context)

# DIRECTOR NEEDS ACTION
def director_needs_action(request, scanned_document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role, id = user_id.split('-')

    if role != 'DIR':
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    selected_documents = request.session.get('selected_documents')

    if selected_documents:
        del request.session['selected_documents']

    if int(scanned_document_no) < 0:

        if id == '1002':
            return render(request, 'director/director-plus-needs-action.html', {'user_profile': user_profile})

        return render(request, 'director/director-needs-action.html', {'user_profile': user_profile})

    try:
        document = Document.objects.get(document_no=scanned_document_no)
    except Document.DoesNotExist:
        scanned_status = "not-found"

        context = {
            'user_profile': user_profile,
            'scanned_status': scanned_status,
        }

        return render(request, 'director/director-needs-action.html', context)

    if document.status == 'For DIR Approval':
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_profile': user_profile,
        'role': role,
        'scanned_document_no': scanned_document_no,
        'scanned_status': scanned_status,
        'document': document,
        'document_details': get_document_details(document)
    }

    return render(request, 'director/director-needs-action.html', context)

# -------------- ACTIVITY LOGS -------------------

# SYSTEM ADMIN AND DIRECTOR ACTIVITY LOGS
def sys_dir_activity_logs(request, activity_type):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role not in ['DIR', 'SYS']:
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    if activity_type == 'doc-management':
        doc_management_logs = DocumentManagementLogs.objects.filter(user_id=user_id).order_by('-time_stamp')
        records = []
        routes = DocumentRoute.objects.all()

        for log in doc_management_logs:
            record = {
                'time_stamp': log.time_stamp,
                'document_no': log.document_type.document_no,
                'document_type': log.document_type.document_type,
                'category': log.document_type.category,
                'priority_level': log.document_type.priority_level.priority_level,
                'routes': [route.route.office_name for route in routes if route.document_type_id == log.document_type.document_no],
                'activity': log.activity
            }
            records.append(record)

        context = {
            'role': role,
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)

    elif activity_type == 'reports':
        records = ReportManagementLogs.objects.filter(user_id=user_id).order_by('-time_stamp')
        context = {
            'role': role,
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)
    
    elif activity_type == 'user-management':
        records = UserManagementLogs.objects.filter(user=user_id).order_by('-time_stamp')
        context = {
            'role': role,
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)
    
    elif activity_type == 'records':
        records = ActivityLogs.objects.filter(user_id_id=user_id).order_by('-time_stamp')
        context = {
            'role': role,
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)

    elif activity_type == 'recent':
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        fifteen_days_start = today_start - timedelta(days=1000)

        document_logs = ActivityLogs.objects.filter(user_id_id=user_id)
        user_management_logs = UserManagementLogs.objects.filter(user=user_id)
        doc_management_logs = DocumentManagementLogs.objects.filter(user_id=user_id)
        report_logs = ReportManagementLogs.objects.filter(user_id=user_id)

        today_logs, yesterday_logs, this_week_logs, last_fifteen_days_logs = [], [], [], []

        def categorize_logs(logs, type_name):
            for log in logs:
                if log.time_stamp >= today_start:
                    today_logs.append({'type': type_name, 'log': log})
                elif yesterday_start <= log.time_stamp < today_start:
                    yesterday_logs.append({'type': type_name, 'log': log})
                elif week_start <= log.time_stamp < yesterday_start:
                    this_week_logs.append({'type': type_name, 'log': log})
                elif fifteen_days_start <= log.time_stamp < week_start:
                    last_fifteen_days_logs.append({'type': type_name, 'log': log})

        categorize_logs(document_logs, 'document')
        categorize_logs(user_management_logs, 'user_management')
        categorize_logs(doc_management_logs, 'doc_management')
        categorize_logs(report_logs, 'report')

        today_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        yesterday_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        this_week_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        last_fifteen_days_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)

        context = {
            'role': role,
            'user_profile': user_profile,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs,
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)

    # Default context if no specific activity_type matches
    context = {
        'role': role,
        'user_profile': user_profile,
        'activity_type': activity_type
    }
    return render(request, 'assets/sys-dir-activity-logs.html', context)

# SRO ACTIVITY LOGS
def sro_activity_logs(request, activity_type):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    if activity_type == 'all-activity':
        records = ActivityLogs.objects.filter(user_id_id=user_id).order_by('-time_stamp')
        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'sro/sro-activity-logs.html', context)
    
    elif activity_type == 'recent':
        
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        fifteen_days_start = today_start - timedelta(days=15)

        records = ActivityLogs.objects.filter(user_id_id=user_id)
        today_logs = []
        yesterday_logs = []
        this_week_logs = []
        last_fifteen_days_logs = []

        for record in records:
            if record.time_stamp >= today_start:
                today_logs.append(record)
            elif yesterday_start <= record.time_stamp < today_start:
                yesterday_logs.append(record)
            elif week_start <= record.time_stamp < yesterday_start:
                this_week_logs.append(record)
            elif fifteen_days_start <= record.time_stamp < week_start:
                last_fifteen_days_logs.append(record)

        today_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        yesterday_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        this_week_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        last_fifteen_days_logs.sort(key=lambda x: x.time_stamp, reverse=True)

        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs
        }

        return render(request, 'sro/sro-activity-logs.html', context)

    context = {
        'user_profile': user_profile,
        'activity_type': activity_type
    }

    return render(request, 'sro/sro-activity-logs.html', context)

# ADMIN OFFICER ACTIVITY LOGS
def admin_officer_activity_logs(request, activity_type):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    if activity_type == 'all-activity':
        records = ActivityLogs.objects.filter(user_id_id=user_id).order_by('-time_stamp')
        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'admin_officer/admin-officer-activity-logs.html', context)
    
    elif activity_type == 'recent':
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        fifteen_days_start = today_start - timedelta(days=15)

        records = ActivityLogs.objects.filter(user_id_id=user_id)
        today_logs = []
        yesterday_logs = []
        this_week_logs = []
        last_fifteen_days_logs = []

        for record in records:
            if record.time_stamp >= today_start:
                today_logs.append(record)
            elif yesterday_start <= record.time_stamp < today_start:
                yesterday_logs.append(record)
            elif week_start <= record.time_stamp < yesterday_start:
                this_week_logs.append(record)
            elif fifteen_days_start <= record.time_stamp < week_start:
                last_fifteen_days_logs.append(record)

        today_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        yesterday_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        this_week_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        last_fifteen_days_logs.sort(key=lambda x: x.time_stamp, reverse=True)

        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs,
        }

        return render(request, 'admin_officer/admin-officer-activity-logs.html', context)

    context = {
        'user_profile': user_profile,
        'activity_type': activity_type,
    }

    return render(request, 'admin_officer/admin-officer-activity-logs.html', context)

# ACTION OFFICER ACTIVITY LOGS
def action_officer_activity_logs(request, activity_type):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    if activity_type == 'all-activity':
        records = ActivityLogs.objects.filter(user_id_id=user_id).order_by('-time_stamp')
        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'action_officer/action-officer-activity-logs.html', context)

    elif activity_type == 'recent':

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        fifteen_days_start = today_start - timedelta(days=15)

        records = ActivityLogs.objects.filter(user_id_id=user_id)
        today_logs = []
        yesterday_logs = []
        this_week_logs = []
        last_fifteen_days_logs = []

        for record in records:
            if record.time_stamp >= today_start:
                today_logs.append(record)
            elif yesterday_start <= record.time_stamp < today_start:
                yesterday_logs.append(record)
            elif week_start <= record.time_stamp < yesterday_start:
                this_week_logs.append(record)
            elif fifteen_days_start <= record.time_stamp < week_start:
                last_fifteen_days_logs.append(record)

        today_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        yesterday_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        this_week_logs.sort(key=lambda x: x.time_stamp, reverse=True)
        last_fifteen_days_logs.sort(key=lambda x: x.time_stamp, reverse=True)

        context = {
            'user_profile': user_profile,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs
        }

        return render(request, 'action_officer/action-officer-activity-logs.html', context)
    
    context = {
        'user_profile': user_profile,
        'activity_type': activity_type
    }

    return render(request, 'action_officer/action-officer-activity-logs.html', context)

# -------------- UNACTED RECORDS -------------------

# DIRECTOR UNACTED RECORDS
def director_unacted_records(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile,
    }
    
    return render(request, 'director/director-unacted-records.html', context)

# SRO UNACTED RECORDS
def sro_unacted_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'sro/sro-unacted-records.html', context)

# ADMIN OFFICER UNACTED RECORDS
def admin_officer_unacted_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'admin_officer/admin-officer-unacted-records.html', context)

# ACTION OFFICER UNACTED RECORDS
def action_officer_unacted_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile
    }

    return render(request, 'action_officer/action-officer-unacted-records.html', context)

# ----------------- RESOLVED RECORDS -------------------

# ADMIN OFFICER RESOLVED RECORDS
def admin_officer_resolved_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    selected_documents = request.session.get('selected_documents')
    if selected_documents:
        del request.session['selected_documents']

    context = {
        'user_profile': user_profile
    }

    return render(request, 'admin_officer/admin-officer-resolved-records.html', context)

def sro_resolved_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    resolved_documents = ActivityLogs.objects.filter(
        activity = 'Document Resolved',
        user_id_id = user_id
    ).order_by('-time_stamp')

    context = {
        'resolved_documents': resolved_documents,
        'user_profile': user_profile
    }

    return render(request, 'sro/sro-resolved-records.html', context)

def action_officer_endorsed_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    endorsed_documents = ActivityLogs.objects.filter(
        activity = 'Document Endorsed by Action Officer',
        user_id_id = user_id
    ).order_by('-time_stamp')

    context = {
        'endorsed_documents': endorsed_documents,
        'user_profile': user_profile
    }

    return render(request, 'action_officer/action-officer-endorsed-records.html', context)


# ---------------- ARCHIVE -------------------

# SYSTEM ADMIN ARCHIVE
def system_admin_archive(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile
    }
    return render(request, 'system_admin/system-admin-archive.html', context)

# DIRECTOR ARCHIVE
def director_archive(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile,
    }
    
    return render(request, 'director/director-archive.html', context)

# ADMIN OFFICER ARCHIVE
def admin_officer_archive(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)
    
    user_profile = request.session.get('user_profile', None)

    context = {
        'user_profile': user_profile
    }

    return render(request, 'admin_officer/admin-officer-archive.html', context)

# ------------------ ANNOUNCEMENTS -----------------------

def system_admin_announcements(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role_prefix = user_id.split('-')[0]
    if role_prefix != 'SYS':
        return redirect('user_login')

    user_profile = request.session.get('user_profile', None)

    if request.method == 'POST':
        title = request.POST.get('announcementTitle')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        offices = request.POST.getlist('offices')  
        all_offices = 'All' in offices
        end_date = request.POST.get('endDate')

        # If no attachment is provided, set it to the default attachment
        if not attachment:
            attachment = 'default_attachment.pdf'  # Ensure this file exists or handle its absence

        # Save the announcement
        announcement = Announcement(
            title=title,
            description=description,
            attachment=attachment,
            offices=', '.join(offices),
            all_offices=all_offices,
            end_date=end_date,
            created_by=user_id  # Assuming this field exists in the model
        )
        announcement.save()
        return redirect('system_admin_announcements')

    # Fetch only the announcements created by the logged-in system administrator
    announcements = Announcement.objects.filter(created_by=user_id)

    # Render the template with announcements and user data
    return render(request, 'system_admin/system-admin-announcements.html', {
        'user_profile': user_profile,
        'announcements': announcements,  # Include announcements in the context
    })

def director_announcements(request):
   
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role_prefix = user_id.split('-')[0]
    if role_prefix != 'DIR':
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    if request.method == 'POST':
        title = request.POST.get('announcementTitle')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        offices = request.POST.getlist('offices')  
        all_offices = 'All' in offices
        end_date = request.POST.get('endDate')

        if not attachment:
            attachment = 'default_attachment.pdf'  # Ensure this file exists or handle its absence

        announcement = Announcement(
            title=title,
            description=description,
            attachment=attachment,
            offices=', '.join(offices),
            all_offices=all_offices,
            end_date=end_date,
            created_by=user_id  # Assuming this field exists in the model
        )
        announcement.save()
        return redirect('director_announcements')

    announcements = Announcement.objects.filter(created_by=user_id)

    # Render the template with announcements and user data
    return render(request, 'director/director-announcements.html', {
        'user_profile': user_profile,
        'announcements': announcements,  # Include announcements in the context
    })

# ------------------ GENERATE REPORTS ------------------

# SYSTEM ADMIN PERFORMANCE REPORTS
def system_admin_performance_reports(request, report_type):    
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)
    
    if report_type == 'all-reports':
        reports = Reports.objects.all()
    elif report_type == 'employee-performance':
        reports = Reports.objects.filter(report_type='Employee Performance')
    elif report_type == 'office-performance':
        reports = Reports.objects.filter(report_type='Office Performance')

    context = {
        'user_profile': user_profile,
        'report_type': report_type,
        'reports': reports,
    }

    return render(request, 'system_admin/system-admin-performance-reports.html', context)

# DIRECTOR PERFORMANCE REPORTS
def director_performance_reports(request, report_type):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    if report_type == 'all-reports':
        reports = Reports.objects.filter(is_active=True)
    elif report_type == 'employee-performance':
        reports = Reports.objects.filter(report_type='Employee Performance', is_active=True)
    elif report_type == 'office-performance':
        reports = Reports.objects.filter(report_type='Office Performance', is_active=True)

    context = {
        'user_profile': user_profile,
        'report_type': report_type,
        'reports': reports
    }

    return render(request, 'director/director-performance-reports.html', context)

# SYSTEM ADMIN PENDING REPORTS
def system_admin_pending_reports(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)
    
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'system_admin/system-admin-pending-reports.html', context)


# DIRECTOR PENDING REPORTS
def director_pending_reports(request, target_user_id):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    admin_officer = User.objects.filter(role='ADO').first()

    users = User.objects.filter(role__in=['SRO', 'ACT'], status='active').annotate(
        role_priority=Case(
            When(role='SRO', then=Value(1)),
            When(role='ACT', then=Value(2)),
        )
    )

    accounting_officers = users.filter(office_id_id='ACC', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    budgeting_officers = users.filter(office_id_id='BMD', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    cashier_officers = users.filter(office_id_id='CSR', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    payroll_officers = users.filter(office_id_id='PRL', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')

    try:

        target_user = User.objects.get(user_id=target_user_id)

        if target_user.role == 'ADO':
            pending_documents = Document.objects.filter(status='For Routing').order_by('-recent_update')
        elif target_user.role == 'SRO':
            pending_documents = Document.objects.filter(
                status__in=['For SRO Receiving', 'For Resolving'], 
                next_route=target_user.office_id_id
            ).order_by('-recent_update')
        elif target_user.role == 'ACT':
            pending_documents = Document.objects.filter(
                status='For ACT Receiving',
                act_receiver=target_user_id
            ).order_by('-recent_update')

        target_user_office = target_user.office_id_id

    except User.DoesNotExist:
        
        target_user_office = 'no-office'
        pending_documents = []

    context = {
        'target_user_id': target_user_id,
        'target_user_office': target_user_office,
        'admin_officer': admin_officer,
        'accounting_officers': accounting_officers,
        'budgeting_officers': budgeting_officers,
        'cashier_officers': cashier_officers,
        'payroll_officers': payroll_officers,
        'user_profile': user_profile,
        'pending_documents': pending_documents
    }

    return render(request, 'director/director-pending-reports.html', context)

# ADMIN OFFICER PENDING REPORTS
def admin_officer_pending_reports(request, target_user_id):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    users = User.objects.filter(role__in=['SRO', 'ACT'], status='active').annotate(
        role_priority=Case(
            When(role='SRO', then=Value(1)),
            When(role='ACT', then=Value(2)),
        )
    )

    accounting_officers = users.filter(office_id_id='ACC', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    budgeting_officers = users.filter(office_id_id='BMD', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    cashier_officers = users.filter(office_id_id='CSR', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')
    payroll_officers = users.filter(office_id_id='PRL', role__in=['SRO', 'ACT']).order_by('role_priority', 'lastname')

    try:

        target_user = User.objects.get(user_id=target_user_id)

        if target_user.role == 'ADO':
            pending_documents = Document.objects.filter(status='For Routing').order_by('-recent_update')
        elif target_user.role == 'SRO':
            pending_documents = Document.objects.filter(
                status__in=['For SRO Receiving', 'For Resolving'],
                next_route=target_user.office_id_id
            ).order_by('-recent_update')
        elif target_user.role == 'ACT':
            pending_documents = Document.objects.filter(
                status='For ACT Receiving',
                act_receiver=target_user_id
            ).order_by('-recent_update')

        target_user_office = target_user.office_id_id

    except User.DoesNotExist:
        
        target_user_office = 'no-office'
        pending_documents = []
    
    context = {
        'target_user_id': target_user_id,
        'target_user_office': target_user_office,
        'accounting_officers': accounting_officers,
        'budgeting_officers': budgeting_officers,
        'cashier_officers': cashier_officers,
        'payroll_officers': payroll_officers,
        'user_profile': user_profile,
        'pending_documents': pending_documents
    }

    return render(request, 'admin_officer/admin-officer-pending-reports.html', context)

# SUB-RECEIVING OFFICER PENDING REPORTS
def sro_pending_reports(request, target_user_id):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    sro_officer = User.objects.get(user_id=user_id)
    
    action_officers = User.objects.filter(role='ACT', status='active', office_id_id=sro_officer.office_id_id)

    try:

        pending_documents = Document.objects.filter(status='For ACT Receiving', act_receiver=target_user_id)

    except User.DoesNotExist:
        
        pending_documents = []
    
    context = {
        'pending_documents': pending_documents,
        'target_user_id': target_user_id,
        'action_officers': action_officers,
        'user_profile': user_profile,
    }

    return render(request, 'sro/sro-pending-reports.html', context)

# ------------- PASSWORD UPDATE -------------------

# Custom token generator
class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp)

account_activation_token = CustomTokenGenerator()

# FORGOT PASSWORD
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_id = request.POST.get('user_id')

        # Verify if the user exists with the provided user_id
        try:
            user = User.objects.get(user_id=user_id)

            # Check if the retrieved user's email matches the provided email
            if user.email != email:
                messages.error(request, "Email does not match the User ID provided.")
                return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        except User.DoesNotExist:
            messages.error(request, "User ID does not match any account.")
            return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        # Check user status
        if user.status not in ['active']:
            messages.error(request, "Your account cannot be used for password reset.")
            return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        # Generate reset link
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        reset_link = request.build_absolute_uri(
            reverse('new_password', kwargs={'uidb64': uidb64, 'token': token})
        )

        # Prepare the HTML email content with inline styles
        try:
            subject = 'Reset your password'
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: 50px auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <div style="background-color: #007BFF; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; color: white;">
                        <h1 style="margin: 0;">TrackIt: Password Reset Request</h1>
                    </div>
                    <div style="padding: 20px; color: #333;">
                        <h2 style="color: #007BFF;">Hello {user.firstname},</h2>
                        <p>Click the reset password below to reset your password:</p>
                        <p><a href="{reset_link}" style="display: inline-block; padding: 12px 25px; font-size: 16px; background-color: #28a745; color: white; border-radius: 5px; text-decoration: none;">Reset Password</a></p>
                        <p>If you did not request a password reset, please ignore this email.</p>
                    </div>
                    <div style="text-align: center; padding: 20px; border-top: 1px solid #dddddd;">
                        <p style="color: #777;">Regards,<br>TrackIt Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            plain_message = strip_tags(html_message)

            # Create and send the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email='noreply@trackit.com',
                to=[user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")

        return render(request, 'forgot-password.html', {'displayForgotPassword': 'd-none', 'displayEmailConfirmation': '', 'displayPasswordSuccess': 'd-none'})

    return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

# NEW PASSWORD
def new_password(request, uidb64, token):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password == confirm_password:
            try:
                # Decode the uid
                uid = force_str(urlsafe_base64_decode(uidb64))
                print(f"Decoded UID: {uid}")
                user = User.objects.get(pk=uid)
                
                # Check the token validity
                is_token_valid = account_activation_token.check_token(user, token)
                print(f"User: {user.firstname}, Token: {token}, Is token valid? {is_token_valid}")
                
                if is_token_valid:
                    # Clear the password (optional)
                    user.password = ""  # This line can be removed if not needed
                    user.password = new_password  # Set new password
                    user.save()
                    return render(request, 'forgot-password.html', {'displayForgotPassword': 'd-none', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': ''}) 
                else:
                    messages.error(request, "The reset link is invalid or expired.")
            except User.DoesNotExist:
                messages.error(request, "Invalid user.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'new-password.html', {'uidb64': uidb64, 'token': token})


# ---------- REUSABLE FUNCTIONS --------------

# SYSTEM ADMIN FUNCTION: EDIT DOCUMENT TYPE
def edit_document_type(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':
        document_no = request.POST.get('edit_document_no')
        document_type = request.POST.get('edit_document_type')
        category = request.POST.get('edit_category')
        priority_level_str = request.POST.get('edit_priority_level')
        route_list = request.POST.getlist('editRoutes[]')
        form_source = request.POST.get('form_source')  # Get the form source

        # Deleting existing document routes
        routes = DocumentRoute.objects.filter(document_type_id=document_no)
        routes.delete()

        priority_level = PriorityLevel.objects.get(priority_level=priority_level_str)

        # Updating document type
        new_document_type = DocumentType.objects.get(document_no=document_no)
        new_document_type.document_type = document_type
        new_document_type.category = category
        new_document_type.priority_level = priority_level
        new_document_type.last_update = timezone.now()
        new_document_type.save()

        DocumentManagementLogs.objects.create(
            time_stamp = timezone.now(),
            document_type=new_document_type,
            activity='Document Type Edited',
            user_id=user_id
        )

        # Adding new document routes
        for route in route_list:
            office = Office.objects.get(office_name=route)
            DocumentRoute.objects.create(document_type_id=new_document_type.document_no, route=office)

        # Redirect based on the form source
        if form_source == 'system_admin':
            return redirect('system_admin_doc_management')
        elif form_source == 'director':
            return redirect('director_doc_management')
        else:
            raise ValueError("Invalid form source provided")  # Raise an error if the form source is unrecognized

    # If it's not a POST request, raise an error or handle appropriately
    raise ValueError("This view only handles POST requests.")

def edit_routes(request):

    if request.method == 'POST':

        document_no = request.POST.get('edit_document_no')
        new_routes = request.POST.getlist('editRoutes[]')
        new_priority_level = request.POST.get('edit_priority_level')
        document_type = request.POST.get('document_type')
        document_category = request.POST.get('document_category')
        
        prio_level = PriorityLevel.objects.get(priority_level=new_priority_level)

        new_document_type = DocumentType.objects.create(
            document_type=document_type,
            category=document_category,
            priority_level_id=prio_level.no,
            is_active = False
        )

        for route in new_routes:

            if route == 'Accounting':
                route_id = 'ACC'
            elif route == 'Director':
                route_id = 'DIR'
            elif route == 'Payroll':
                route_id = 'PRL'
            elif route == 'Cashier':
                route_id = 'CSR'
            elif route == 'Budgeting':
                route_id = 'BMD'
            
            DocumentRoute.objects.create(
                document_type = new_document_type,
                route_id = route_id
            )

        document = Document.objects.get(document_no=document_no)
        document.document_type = new_document_type
        document.save()

    return JsonResponse({'success': 'success'})




# SYSTEM ADMIN FUNCTION: DELETE DOCUMENT TYPE
def delete_document_type(request, document_no):

    """routes = DocumentRoute.objects.filter(document_type_id = document_no)
    routes.delete()
    document_type = DocumentType.objects.get(document_no=document_no)
    document_type.delete()"""

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('user_login')

    document_type = DocumentType.objects.get(document_no=document_no)
    document_type.is_active = False
    document_type.save()

    DocumentManagementLogs.objects.create(
        time_stamp = timezone.now(),
        document_type=document_type,
        activity='Document Type Deleted',
        user_id=user_id
    )

    role = user_id.split('-')[0]
    if role == 'DIR':
        return redirect(director_doc_management)
    else:
        return redirect(system_admin_doc_management)

# LOADING OF DOC TYPES
def load_document_types(request):
    category = request.GET.get('category')

    if category in ['Trust', 'Regular']:
        document_types = DocumentType.objects.filter(category=category, is_active=True).values('document_no', 'document_type')
        return JsonResponse(list(document_types), safe=False)
    else:
        return JsonResponse({'error': 'Invalid category'}, status=400)

def mask_password(password):
    if len(password) <= 2:
        return '*' * len(password)  # Fully mask short passwords
    return password[0] + '*' * (len(password) - 2) + password[-1]

#USER UPDATE STATUS AND EMAILING FUNCTION
def update_user_status(request, user_id, action, office, user_type):

    loggedin_user_id = request.session.get('user_id')
    if not loggedin_user_id:
        return redirect('user_login')
    
    user = User.objects.get(pk=user_id)
    login_url = request.build_absolute_uri(reverse("user_login"))
    
    # Perform action and define subject & message
    if action == 'verify':
        activity = 'User Verified'
        user.status = 'active'
        subject = 'TrackIt: Your Account Has Been Verified'

        masked_password = mask_password(user.password)

        # HTML message for account verification
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Verified</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Your account has been verified and is now active.</p>
                    <p><strong>User ID:</strong> {user.user_id}</p>
                    <p><strong>Password:</strong> {masked_password}</p>
                    <p>Please keep this information secure.</p>
                    <p>
                        <a href="{login_url}" class="button">Go to TrackIt</a>
                    </p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        plain_message = strip_tags(html_message)

    elif action == 'reject':
        activity = 'User Rejected'
        user.status = 'rejected'
        subject = 'TrackIt: Your Account Has Been Rejected'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Rejected</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Unfortunately, your account has been rejected. Please contact support for more information.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'deactivate':
        activity = 'User Deactivated'
        user.status = 'inactive'
        subject = 'TrackIt: Your Account Has Been Deactivated'
        html_message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    line-height: 1.6;
                    color: #333;
                }}
                .email-container {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: 50px auto;
                    overflow: hidden;
                }}
                .email-header {{
                    background-color: #7F7F7F; 
                    padding: 20px;
                    text-align: center;
                    color: #fff;
                    font-size: 24px;
                    font-weight: bold;
                    border-radius: 10px 10px 0 0;
                }}
                .email-content {{
                    padding: 30px;
                    font-size: 16px;
                    color: #555;
                }}
                .email-content p {{
                    margin: 0 0 20px;
                }}
                .email-content h1 {{
                    font-size: 22px;
                    margin-bottom: 10px;
                    color: #007BFF;
                }}
                .email-footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-top: 1px solid #dddddd;
                    font-size: 14px;
                    color: #777777;
                }}
                .email-footer p {{
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Deactivated</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Your account has been deactivated. Please contact support if you wish to reactivate it.</p>
                    <p>If you have any questions, feel free to reach out.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'archive':
        activity = 'User Archived'
        user.status = 'archived'
        subject = 'TrackIt: Your Account Has Been Archived'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Archived</h1>
                </div>
                <div class="email-content">
                    <p>Your account has been archived and you will not be able to log in anymore.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'reactivate':
        activity = 'User Reactivated'
        user.status = 'active'
        subject = 'TrackIt: Your Account Has Been Reactivated'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Reactivated</h1>
                </div>
                <div class="email-content">
                    <p>Your account has been reactivated and is now active.</p>
                    <p>
                        <a href="{login_url}" class="button">Go to TrackIt</a>
                    </p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    else:
        return HttpResponse("Invalid action", status=400)

    user.save()

    UserManagementLogs.objects.create(
        time_stamp = timezone.now(),
        employee=user,
        activity=activity,
        user=loggedin_user_id
    )

    # Send the email using EmailMultiAlternatives
    """email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)"""

    role = loggedin_user_id.split('-')[0]
    # Redirect based on the form source
    if role == 'DIR':
        return redirect('director_user_management', office=office)
    else:
        print('system admin')
        return redirect('system_admin_user_management', office=office)

    loggedin_user_id = request.session.get('user_id')
    if not loggedin_user_id:
        return redirect('user_login')
    
    user = User.objects.get(pk=user_id)
    login_url = request.build_absolute_uri(reverse("user_login"))

    # Perform action and define subject & message
    if action == 'verify':
        activity = 'User Verified'
        user.status = 'active'
        subject = 'TrackIt: Your Account Has Been Verified'

        # HTML message for account verification
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Verified</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Your account has been verified and is now active.</p>
                    <p><strong>User ID:</strong> {user.user_id}</p>
                    <p><strong>Password:</strong> {user.password}</p>
                    <p>Please keep this information secure.</p>
                    <p>
                        <a href="{login_url}" class="button">Go to TrackIt</a>
                    </p>

                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        plain_message = strip_tags(html_message)

    elif action == 'reject':
        activity = 'User Rejected'
        user.status = 'rejected'
        subject = 'TrackIt: Your Account Has Been Rejected'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Rejected</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Unfortunately, your account has been rejected. Please contact support for more information.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'deactivate':
        activity = 'User Deactivated'
        user.status = 'inactive'
        subject = 'TrackIt: Your Account Has Been Deactivated'
        html_message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    line-height: 1.6;
                    color: #333;
                }}
                .email-container {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    margin: 50px auto;
                    overflow: hidden;
                }}
                .email-header {{
                    background-color: #7F7F7F; 
                    padding: 20px;
                    text-align: center;
                    color: #fff;
                    font-size: 24px;
                    font-weight: bold;
                    border-radius: 10px 10px 0 0;
                }}
                .email-content {{
                    padding: 30px;
                    font-size: 16px;
                    color: #555;
                }}
                .email-content p {{
                    margin: 0 0 20px;
                }}
                .email-content h1 {{
                    font-size: 22px;
                    margin-bottom: 10px;
                    color: #007BFF;
                }}
                .email-footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-top: 1px solid #dddddd;
                    font-size: 14px;
                    color: #777777;
                }}
                .email-footer p {{
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Deactivated</h1>
                </div>
                <div class="email-content">
                    <p>Hello {user.firstname},</p>
                    <p>Your account has been deactivated. Please contact support if you wish to reactivate it.</p>
                    <p>If you have any questions, feel free to reach out.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'archive':
        activity = 'User Archived'
        user.status = 'archived'
        subject = 'TrackIt: Your Account Has Been Archived'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Archived</h1>
                </div>
                <div class="email-content">
                    <p>Your account has been archived and you will not be able to log in anymore.</p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    elif action == 'reactivate':
        activity = 'User Reactivated'
        user.status = 'active'
        subject = 'TrackIt: Your Account Has Been Reactivated'
        html_message = f"""
        <html>
        <head>{common_style}</head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>TrackIt: Account Reactivated</h1>
                </div>
                <div class="email-content">
                    <p>Your account has been reactivated and is now active.</p>
                    <p>
                        <a href="{login_url}" class="button">Go to TrackIt</a>
                    </p>
                </div>
                <div class="email-footer">
                    <p>Regards,<br>TrackIt Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

    else:
        return HttpResponse("Invalid action", status=400)

    user.save()

    UserManagementLogs.objects.create(
        time_stamp = timezone.now(),
        employee=user,
        activity=activity,
        user=loggedin_user_id
    )

    # Send the email using EmailMultiAlternatives
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

    role = loggedin_user_id.split('-')[0]
    # Redirect based on the form source
    if role == 'DIR':
        return redirect('director_user_management', office=office)
    else:
        print('system admin')
        return redirect('system_admin_user_management', office=office)


# GENERATE USER ID (USER SIGN UP)
def generate_user_id(role_prefix):
    max_user_id = User.objects.filter(user_id__startswith=f"{role_prefix}-").aggregate(max_id=Max('user_id'))['max_id']
    if max_user_id:
        max_number = int(max_user_id.split('-')[1])
        new_number = max_number + 1
    else:
        new_number = 1000
    return f"{role_prefix}-{new_number:04d}"

# CREATE DOCUMENT (NEW RECORD MODULE)
def create_document(tracking_no, sender_name, sender_dept, doc_type, subject, remarks, file_attachment, user_id):

    document_type_instance = DocumentType.objects.get(document_no=doc_type)
    document_type_instance.used_count += 1
    document_type_instance.save()

    days_deadline = document_type_instance.priority_level.deadline
    ongoing_deadline = date.today() + timedelta(days=days_deadline)

    document = Document.objects.create(
        tracking_no=tracking_no,
        sender_name=sender_name,
        sender_department=sender_dept,
        document_type=document_type_instance,
        subject=subject,
        remarks=remarks,
        status='For DIR Approval',
        recent_update = timezone.now(),
        ongoing_deadline=ongoing_deadline
    )

    new_remarks = Remarks.objects.create(
        remarks=remarks
    )

    # Create ActivityLogs entry with default user_id from the session
    ActivityLogs.objects.create(
        time_stamp=timezone.now(),
        activity='Document Created',
        document_id=document,
        user_id_id=user_id,
        remarks = new_remarks,
        receiver_id_id = 'DIR-1001',
        file_attachment = file_attachment
    )

    return document

# OUTPUT ROUTES IN STRINGS FORMAT
def generate_route_strings(routes):
    str_routes = ''
    str_routes_titles = ''
    
    for index, route in enumerate(routes):
        str_routes += route.route_id
        str_routes_titles += route.route.office_name
        
        if index < len(routes) - 1:
            str_routes += '-'
            str_routes_titles += ' - '
            
    return str_routes, str_routes_titles

# GENERATE QR CODE (NEW RECORD)
def generate_qr_code(request, document_no):
    print("pumasok sa generate_qr_code views ")
    # Define the URL to be encoded in the QR code
    url = request.build_absolute_uri(f'/scanned-qr-code/{document_no}/')

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Save to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type='image/png')

def get_routes(request, document_no):

    try:
        document = Document.objects.get(document_no=document_no)

        routes = DocumentRoute.objects.filter(document_type_id = document.document_type_id)
        str_routes, str_routes_titles = generate_route_strings(routes)

        data = {
            'str_routes': str_routes,
            'str_routes_titles': str_routes_titles
        }

        return JsonResponse(data)

    except Document.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

def search_document_type(document_types, search_query):

    document_types = document_types.filter(
            Q(document_type__icontains=search_query)
        )
    
    for doc_type in document_types:

        if search_query in doc_type.document_type:
            doc_type.highlighted_document_type = doc_type.document_type.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
            print(doc_type.highlighted_document_type)
        else:
            doc_type.highlighted_document_type = doc_type.document_type
    
    return document_types

def search_documents(documents, search_query):

    documents = documents.filter(
            Q(tracking_no__icontains=search_query) |
            Q(sender_name__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(remarks__icontains=search_query) 
        )
  
    for document in documents:

        if search_query in document.tracking_no:
            document.highlighted_tracking_no = document.tracking_no.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            document.highlighted_tracking_no = document.tracking_no

        if search_query in document.sender_name:
            document.highlighted_sender_name = document.sender_name.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            document.highlighted_sender_name = document.sender_name

        if search_query in document.subject:
            document.highlighted_subject = document.subject.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            document.highlighted_subject = document.subject

    return documents

def search_unacted_documents(unacted_logs, search_query):

    unacted_logs = unacted_logs.filter(
            Q(document_id__tracking_no__icontains=search_query) |
            Q(document_id__sender_name__icontains=search_query) |
            Q(document_id__subject__icontains=search_query) |
            Q(document_id__remarks__icontains=search_query) 
        )

    for log in unacted_logs:

        if search_query in log.document_id.tracking_no:
            log.document_id.highlighted_tracking_no = log.document_id.tracking_no.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            log.document_id.highlighted_tracking_no = log.document_id.tracking_no

        if search_query in log.document_id.sender_name:
            log.document_id.highlighted_sender_name = log.document_id.sender_name.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            log.document_id.highlighted_sender_name = log.document_id.sender_name

        if search_query in log.document_id.subject:
            log.document_id.highlighted_subject = log.document_id.subject.replace(
                search_query, f"<span class='highlight-search'>{search_query}</span>"
            )
        else:
            log.document_id.highlighted_subject = log.document_id.subject

    return unacted_logs

# SORTINGGG

def sort_documents(documents, sort_by, order, status):
    if sort_by == 'status':
        if order == 'asc':
            documents = documents.order_by(sort_by)
        else:
            documents = documents.order_by(f'-{sort_by}')
    else:
        if sort_by == 'document_type':
            if status == 'For DIR Approval':
                documents = Document.objects.filter(status="For DIR Approval").order_by('document_type__category')
            elif status == 'For Routing':
                documents = Document.objects.filter(status="For Routing").order_by('document_type__category')
            elif status == 'For Archiving':
                documents = Document.objects.filter(status="For Archiving").order_by('document_type__category')
            elif status == 'ADO - All Documents':
                documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving"]).order_by('document_type__category')
            else:
                documents = Document.objects.exclude(status="Archived").order_by('document_type__category')

        elif sort_by == 'deadline':
            if status == 'For DIR Approval':
                documents = Document.objects.filter(status="For DIR Approval").order_by('document_type__priority_level__deadline')
            elif status == 'For Routing':
                documents = Document.objects.filter(status="For Routing").order_by('document_type__priority_level__deadline')
            elif status == 'For Archiving':
                documents = Document.objects.filter(status="For Archiving").order_by('document_type__priority_level__deadline')
            elif status == 'ADO - All Documents':
                documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving"]).order_by('document_type__priority_level__deadline')
            else:
                documents = Document.objects.exclude(status="Archived").order_by('document_type__priority_level__deadline')

        else:
            if status == 'For DIR Approval':
                documents = Document.objects.filter(status="For DIR Approval").order_by('document_type__priority_level__priority_level')
            elif status == 'For Routing':
                documents = Document.objects.filter(status="For Routing").order_by('document_type__priority_level__priority_level')
            elif status == 'For Archiving':
                documents = Document.objects.filter(status="For Archiving").order_by('document_type__priority_level__priority_level')
            elif status == 'ADO - All Documents':
                documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving"]).order_by('document_type__priority_level__priority_level')
            else:
                documents = Document.objects.exclude(status="Archived").order_by('document_type__priority_level__priority_level')

    return documents

def sort_documents_sro(documents, sort_by, order, status, next_route):

    if sort_by == 'status':
        if order == 'asc':
            documents = documents.order_by(sort_by)
        else:
            documents = documents.order_by(f'-{sort_by}')
    else:

        # For Type
        if sort_by == 'document_type':
            if status == 'For ACT Forwarding':
                documents = Document.objects.filter(status="For SRO Receiving", next_route=next_route).order_by('document_type__category')
            elif status == 'For ACT Receiving':
                documents = Document.objects.filter(status="For ACT Receiving", next_route=next_route).order_by('document_type__category')
            elif status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__category')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving", "For ACT Receiving"], next_route=next_route).order_by('document_type__category')
        # For Due
        elif sort_by == 'deadline':
            if status == 'For ACT Forwarding':
                documents = Document.objects.filter(status="For SRO Receiving", next_route=next_route).order_by('document_type__priority_level__deadline')
            if status == 'For ACT Receiving':
                documents = Document.objects.filter(status="For ACT Receiving", next_route=next_route).order_by('document_type__priority_level__deadline')
            if status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__priority_level__deadline')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For ACT Receiving", "For Resolving"], next_route=next_route).order_by('document_type__priority_level__deadline')
        # For Priority Level
        else:
            if status == 'For ACT Forwarding':
                documents = Document.objects.filter(status="For SRO Receiving", next_route=next_route).order_by('document_type__priority_level__priority_level')
            if status == 'For ACT Receiving':
                documents = Document.objects.filter(status="For ACT Receiving", next_route=next_route).order_by('document_type__priority_level__priority_level')
            elif status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__priority_level__priority_level')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For ACT Receiving", "For Resolving"], next_route=next_route).order_by('document_type__priority_level__priority_level')

    return documents

def sort_documents_act(documents, sort_by, order, user_id):

    if sort_by == 'status':
        if order == 'asc':
            documents = documents.order_by(sort_by)
        else:
            documents = documents.order_by(f'-{sort_by}')
    else:
        if sort_by == 'document_type':
            documents = Document.objects.filter(status="For ACT Receiving", act_receiver=user_id).order_by('document_type__category')
        elif sort_by == 'deadline':
            documents = Document.objects.filter(status="For ACT Receiving", act_receiver=user_id).order_by('document_type__priority_level__deadline')
        else:
            documents = Document.objects.filter(status="For ACT Receiving", act_receiver=user_id).order_by('document_type__priority_level__priority_level')

    return documents

# FILTERINGGG

def filter_records(request):

    if request.method == 'POST':

        body = json.loads(request.body)

        statuses = body.get('status', [])
        types = body.get('type', [])
        priorities = body.get('priority', [])

        if statuses or types or priorities:

            filter_documents = {
                'statuses': statuses,
                'types': types,
                'priorities': priorities
            }

        else:
            filter_documents = {}

        request.session['filter_documents'] = filter_documents

    data = {
        'success': 'success'
    }

    return JsonResponse(data)

def remove_filter(request):

    filter_documents = request.session.get('filter_documents')
    if filter_documents:
        del request.session['filter_documents']

    data = {
        'success': 'success'
    }

    return JsonResponse(data)



def scanning_qr_code(request, document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    user_role = user_id.split('-')[0]

    if user_role == 'DIR':
        return redirect('director_needs_action', scanned_document_no=document_no)
    elif user_role == 'ADO':
        return redirect('admin_officer_needs_action', panel='all-documents', scanned_document_no=document_no)
    elif user_role == 'SRO':
        return redirect('sro_records', panel='All-Documents', scanned_document_no=document_no)
    elif user_role == 'ACT':
        return redirect('action_officer_records', scanned_document_no=document_no)

# FUNCTION FOR ALL ACTIONS (APPROVE, ROUTE, ARCHIVED...)
def document_update_status(request, action, document_no):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    document = Document.objects.get(document_no=document_no)
    act_receiver = ''

    if action == 'approve':
        
        routes = DocumentRoute.objects.filter(document_type_id=document.document_type_id)

        if document.next_route:

            current_route = document.next_route
            routes_list = list(routes.values_list('route_id', flat=True))

            try:
                current_route_index = routes_list.index(current_route)
            except ValueError:
                current_route_index = -1

            # Check if it's the last route
            if current_route_index != -1 and current_route_index < len(routes_list) - 1:
                # If it's not the last route, assign the next route
                next_route = routes_list[current_route_index + 1]
                document.next_route = next_route
                status = 'For SRO Receiving'
                user = User.objects.filter(role='SRO', office_id_id=next_route, status='active').first()
                act_receiver = user.user_id
            else:
                # If it's the last route
                status = 'For Archiving'
                act_receiver = 'ADO-1001'

        else:

            if routes.count() == 1 and routes.first().route_id == 'DIR':
                status = 'For Archiving'
            else:
                status = 'For Routing'
            
            act_receiver = 'ADO-1001'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)

        activity = 'Document Approved'

    elif action == 'reject':

        status = 'Rejected'
        activity = 'Document Rejected'
        document.is_rejected = True
        act_receiver = 'ADO-1001'

    elif action == 'route':

        status = 'For SRO Receiving'
        activity = 'Document Routed'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)

        if not document.next_route:
            first_route = DocumentRoute.objects.filter(document_type=document.document_type).first()
            document.next_route = first_route.route_id

    elif action == 'forward':

        status = 'For ACT Receiving'
        activity = 'Document Forwarded to Action Officer'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)

        office = document.next_route
        initial_officer = User.objects.filter(office_id_id = office, role = 'ACT', receive_recent = 0, status='active').first()

        #if wala, it means lahat na ng ACTO ay nakareceive, so reset nya
        if initial_officer == None:
            officers = User.objects.filter(office_id_id = office, role = 'ACT', status='active')

            for index, officer in enumerate(officers):
                officer.receive_recent = False
                if index == 0:
                    #pagka reset, matic yung unang user yung tatanggap
                    officer.receive_recent = True
                    document.act_receiver = officer.user_id
                    officer.save()
                else:
                    officer.receive_recent = False
                    officer.save()
                    
        else:
            initial_officer.receive_recent = True
            initial_officer.save()
            document.act_receiver = initial_officer.user_id

    elif action == 'endorse':
        status = 'For Resolving'
        activity = 'Document Endorsed by Action Officer'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)

    elif action == 'resolve':
        
        routes = DocumentRoute.objects.filter(document_type_id=document.document_type_id)

        if routes.count() > 1:
            print("more than one routes")
            current_route = document.next_route
            routes_list = list(routes.values_list('route_id', flat=True))

            try:
                current_route_index = routes_list.index(current_route)
            except ValueError:
                print("Current route not found in the route list.")
                current_route_index = -1

            # Check if it's the last route
            if current_route_index != -1 and current_route_index < len(routes_list) - 1:
                # If it's not the last route, assign the next route
                next_route = routes_list[current_route_index + 1]
                document.next_route = next_route

                if next_route == 'DIR':
                    status = 'For DIR Approval'
                    #act_receiver = User.objects.get(status='active', role='Director').user_id
                    act_receiver = 'DIR-1001'
                else:
                    status = 'For SRO Receiving'
                    act_receiver = User.objects.get(status='active', role='SRO', office_id_id=next_route).user_id

            else:
                # If it's the last route
                print("Last route reached")
                status = 'For Archiving'
                act_receiver = 'ADO-1001'
        else:
            print("1 route only")
            status = 'For Archiving'
            act_receiver = 'ADO-1001'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)
        
        activity = 'Document Resolved'

    elif action == 'archive':
        status = 'Archived'
        activity = 'Document Archived'
        
        if document.old_document_type:
            document_type_no = document.document_type.document_no
            document.document_type_id = document.old_document_type
            document.save()
            routes = DocumentRoute.objects.filter(document_type_id=document_type_no)
            routes.delete()
            document_type = DocumentType.objects.get(document_no=document_type_no)
            document_type.delete()

    elif action == 'delete':

        logs = ActivityLogs.objects.filter(document_id=document)
        # Delete remarks related to each log
        for log in logs:
            if log.remarks_id:
                Remarks.objects.filter(no=log.remarks_id).delete()  # Directly delete the related remark
        # Bulk delete all logs after processing remarks
        logs.delete()

        unacted_logs = UnactedLogs.objects.filter(document_id=document)
        unacted_logs.delete()

        try:
            document.delete()
        except Document.DoesNotExist:
            data = {'error': 'Document not found'}
            return JsonResponse(data, status=404)

        folder_path = os.path.join(settings.MEDIA_ROOT, f'document/{document_no}')

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

        data = {'success': 'delete success'}
        return JsonResponse(data, status=404)

    if document.status in ['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For Resolving']:
        unacted_log = UnactedLogs.objects.filter(status=document.status, document_id=document).first()
        if unacted_log:
            unacted_log.is_acted = True
            unacted_log.date_acted = timezone.now().date()
            unacted_log.save()   

    document.status = status
    document.recent_update = timezone.now()
    document.save()

    if action == 'forward':
        act_receiver = document.act_receiver
    elif action == 'route':
        sro = User.objects.get(status='active', role='SRO', office_id_id=document.next_route)
        act_receiver = sro.user_id
    elif action == 'endorse':
        sro = User.objects.get(status='active', role='SRO', office_id_id=document.next_route)
        act_receiver = sro.user_id

    new_remarks = Remarks.objects.create(
        remarks=""
    )

    log = ActivityLogs.objects.create(
        time_stamp=timezone.now(),
        activity=activity,
        document_id=document,
        user_id_id=user_id,
        remarks = new_remarks,
        receiver_id_id = act_receiver if act_receiver else None
    )
    data = {
        'remarks_no': log.remarks_id,
        'activity_log_no': log.no
        }
    return JsonResponse(data)

    #approve = For Routing
    #route = For SRO Receiving
    #forward-to-act = For ACT Receiving
    #endorse-for-resolve = For Resolving
    #resolve = For Archiving
    #archive = Archived

def document_multiple_update_status(request, action):

    if request.method == 'POST':
        body = json.loads(request.body)

        documents_no = list(map(int, body.get('checkedValues', [])))

        for no in documents_no:

            document_update_status(request, action, no)



        # For SRO Receiving, For Routing, For Archiving



    data = {
        "success": "success"
    }

    return JsonResponse(data)


def add_remarks(request, document_no, remarks_no):

    if request.method == 'POST':
        
        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')

        editRemarks = Remarks.objects.get(no=remarks_no)
        editRemarks.remarks = remarks
        editRemarks.save()
        
        document = Document.objects.get(document_no=document_no)
        document.remarks = remarks
        document.save()

        if file_attachment:
            activity_log = ActivityLogs.objects.get(remarks_id=remarks_no)
            folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(document_no))
            file_attachment = handle_file_versioning(file_attachment, folder_path)
            activity_log.file_attachment = file_attachment
            activity_log.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_empty_remarks(request):
    Remarks.objects.filter(Q(remarks="") | Q(remarks__isnull=True)).delete()
    data = {}
    return JsonResponse(data)

def get_document_details(document):

    d_type = document.document_type.category
    d_type = d_type[0].upper() + d_type[1:]
    d_type += " - " + document.document_type.document_type.title()

    routes_txt = ""

    if document.status != 'For DIR Approval':

        routes = DocumentRoute.objects.filter(document_type_id=document.document_type_id)

        for index, route in enumerate(routes):
            routes_txt += route.route.office_name
            if index < len(routes) - 1: 
                routes_txt += ' - '


    data = {
        'tracking_no': document.tracking_no,
        'sender_name': document.sender_name.title(),
        'status': document.status,
        'document_type': d_type,  # Assuming foreign key
        'priority': document.document_type.priority_level.priority_level.title(),
        'subject': document.subject,
        'routes_txt': routes_txt
    }

    log_entries = []

    activity_logs = ActivityLogs.objects.filter(document_id=document).order_by('-time_stamp')
    
    for activity in activity_logs:
        manila_tz = pytz.timezone('Asia/Manila')
        local_time = activity.time_stamp.astimezone(manila_tz)

        firstname = activity.user_id.firstname.title()
        middlename = (activity.user_id.middlename[0].capitalize() + '.' if activity.user_id.middlename else '')
        lastname = activity.user_id.lastname.capitalize()
        role = activity.user_id.role

        if role in ['ADO', 'SRO', 'ACT', 'Director', 'System Admin']:
            office = activity.user_id.office_id.office_name
        else:
            office = ""
        
        if role == 'ADO':
            role = 'Admin Officer'
        elif role == 'SRO':
            role = 'Sub-Receiving Officer'
        elif role == 'ACT':
            role = 'Action Officer'
        

        if activity.remarks is None:
            remarks = ""
        else:
            remarks = activity.remarks.remarks

        file_attachment = activity.file_attachment.url if activity.file_attachment else ''

        receiver_name = ""

        if activity.activity != "Document Archived":

            receiver_name += activity.receiver_id.firstname + " " + activity.receiver_id.lastname

        log = {
            'date': local_time.strftime('%Y-%m-%d'),
            'time': local_time.strftime('%I:%M %p').lstrip('0'),
            'employee_id': activity.user_id.employee_id,
            'name': f"{firstname} {middlename} {lastname}".strip(),
            'office': office,
            'role': role,
            'remarks': remarks,
            'file_attachment': file_attachment,
            'activity': activity.activity,
            'receiver_name': receiver_name,
            'user_id': activity.user_id_id
        }
        log_entries.append(log)

    data['activity_logs'] = log_entries

    return data

# ---------- FETCHING --------------

def fetch_document_details(request, document_no):

    document = Document.objects.get(document_no=document_no)
    data = get_document_details(document)

    return JsonResponse(data)


# ---------- PARTIALS --------------

def update_document_types_display(request):

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    records = []

    document_type_records = DocumentType.objects.filter(is_active=True)

    if search_query:
        document_type_records = search_document_type(document_type_records, search_query)

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if sort_by in ['document_type', 'category', 'priority_level_id', 'email']:
        if order == 'asc':
            document_type_records = document_type_records.order_by(sort_by)
        else:
            document_type_records = document_type_records.order_by(f'-{sort_by}')

    routes = DocumentRoute.objects.all()

    for document_type_record in document_type_records:
        record = {
            'document_no': document_type_record.document_no,
            'category': document_type_record.category,
            'priority_level': document_type_record.priority_level.priority_level,
            'routes': [route.route.office_name for route in routes if route.document_type_id == document_type_record.document_no]
        }
        if search_query:
            record['document_type'] = document_type_record.highlighted_document_type
        else:
            record['document_type'] =document_type_record.document_type

        records.append(record)

    context = {
        'search_query': search_query,
        'records': records
    }

    html = render_to_string('partials/display-document-types.html', context)
    return JsonResponse({'html': html})

def update_user_display(request, office):

    search_query = request.GET.get('search', '').strip()

    if office == 'all-office':
        users = User.objects.exclude(status='archived').order_by('-registered_date')
    elif office == 'administrative':
        office_instance  = Office.objects.get(office_id='ADM')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived').order_by('-registered_date')
    elif office == 'accounting':
        office_instance  = Office.objects.get(office_id='ACC')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived').order_by('-registered_date')
    elif office == 'budgeting':
        office_instance  = Office.objects.get(office_id='BMD')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived').order_by('-registered_date')
    elif office == 'cashier':
        office_instance  = Office.objects.get(office_id='CSR')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived').order_by('-registered_date')
    elif office == 'payroll':
        office_instance  = Office.objects.get(office_id='PRL')
        users = User.objects.filter(office_id=office_instance).exclude(status='archived').order_by('-registered_date')
    else:
        users = User.objects.none()

     # Exclude the user with user_id 'SYS-0001'
    users = users.exclude(user_id='SYS-0001')
    users = users.exclude(user_id='DIR-0001')

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    # Search filter
    if search_query:
        users = users.filter(
            Q(firstname__icontains=search_query) |
            Q(middlename__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(contact_no__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )

        for user in users:

            if search_query in user.employee_id:
                user.highlighted_employee_id = user.employee_id.replace(
                    search_query, f"<span class='highlight-search'>{search_query}</span>"
                )
            else:
                user.highlighted_employee_id = user.employee_id

            firstname = user.firstname.title()
            middlename = (user.middlename[0].capitalize() + '.' if user.middlename else '')
            lastname = user.lastname.capitalize()
            fullname = f"{firstname} {middlename} {lastname}".strip()
            
            if search_query in fullname:
                user.highlighted_fullname = fullname.replace(
                    search_query, f"<span class='highlight-search'>{search_query}</span>"
                )
            else:
                user.highlighted_fullname = fullname

            if search_query in user.contact_no:
                user.highlighted_contact_no = user.contact_no.replace(
                    search_query, f"<span class='highlight-search'>{search_query}</span>"
                )
            else:
                user.highlighted_contact_no = user.contact_no

            if search_query in user.email:
                user.highlighted_email = user.email.replace(
                    search_query, f"<span class='highlight-search'>{search_query}</span>"
                )
            else:
                user.highlighted_email = user.email


    if sort_by in ['role', 'status', 'lastname', 'email']:  # Only allow sorting by valid fields
        if order == 'asc':
            users = users.order_by(sort_by)
        else:
            users = users.order_by(f'-{sort_by}')

    context = {
        'users': users,
        'office': office,
        'search_query': search_query,
    }    

    html = render_to_string('partials/system-admin-users.html', context)
    return JsonResponse({'html': html})

def update_all_records_display(request, user):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    id = user_id.split('-')[1]

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    most_priority_doc_type = DocumentType.objects.filter(priority_level__priority_level='very urgent').order_by('-used_count').first()

    documents = Document.objects.exclude(status='archived').order_by('-recent_update')

    # FILTERING:
    filter_documents = request.session.get('filter_documents')  

    if filter_documents:

        filter_status = filter_documents.get('statuses', [])
        filter_type = filter_documents.get('types', [])
        filter_priority = filter_documents.get('priorities', [])

        if filter_status:
            documents = documents.filter(status__in=filter_status)
        if filter_type:
            documents = documents.filter(document_type__category__in=filter_type)
        if filter_priority:
            documents = documents.filter(document_type__priority_level__priority_level__in=filter_priority)

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, "All Records")

    context = {
        'documents': documents,
        'most_priority_doc_type': most_priority_doc_type,
        'search_query': search_query,
        'user': user,
        'today': date.today(),
        'id': id
    }

    html = render_to_string('partials/display-records.html', context)
    return JsonResponse({'html': html})

def admin_officer_update_needs_action_display(request, panel):

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    selection = False

    selected_documents = request.session.get('selected_documents', [])

    if panel == 'For-DIR-Approval':
        documents = Document.objects.filter(status__in=['For DIR Approval', 'Rejected'], next_route=None).order_by('-recent_update')
        status = "For DIR Approval"
    elif panel == 'For-Routing':
        selection = True
        documents = Document.objects.filter(status='For Routing').order_by('-recent_update')
        status = "For Routing"
    elif panel == 'For-Archiving':
        selection = True
        documents = Document.objects.filter(status='For Archiving').order_by('-recent_update')
        status = "For Archiving"
    else:
        documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving", "Rejected"]).order_by('-recent_update')
        status = "ADO - All Documents"

    # FILTERING:
    filter_documents = request.session.get('filter_documents')  

    if filter_documents:

        filter_type = filter_documents.get('types', [])
        filter_priority = filter_documents.get('priorities', [])

        if filter_type:
            documents = documents.filter(document_type__category__in=filter_type)
        if filter_priority:
            documents = documents.filter(document_type__priority_level__priority_level__in=filter_priority)

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, status)

    context = {
        'selection': selection,
        'selected_documents': selected_documents,
        'documents': documents,
        'search_query': search_query,
        'user': 'ADO',
        'today': date.today() 
    }

    html = render_to_string('partials/display-records-with-mult-update.html', context)
    return JsonResponse({'html': html})

def director_update_needs_action_display(request):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    id = user_id.split('-')[1]

    selected_documents = request.session.get('selected_documents', [])

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    most_priority_doc_type = DocumentType.objects.filter(priority_level__priority_level='very urgent').order_by('-used_count').first()
    
    documents = Document.objects.filter(status='For DIR Approval').order_by('-recent_update')

    # FILTERING:
    filter_documents = request.session.get('filter_documents')  

    if filter_documents:

        filter_type = filter_documents.get('types', [])
        filter_priority = filter_documents.get('priorities', [])

        if filter_type:
            documents = documents.filter(document_type__category__in=filter_type)
        if filter_priority:
            documents = documents.filter(document_type__priority_level__priority_level__in=filter_priority)

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, "For DIR Approval")

    context = {
        'documents': documents,
        'selection': True,
        'selected_documents': selected_documents,
        'most_priority_doc_type': most_priority_doc_type,
        'search_query': search_query,
        'user': 'DIR',
        'today': date.today(),
        'id': id
    }

    html = render_to_string('partials/display-records-with-mult-update.html', context)
    return JsonResponse({'html': html})

def sro_update_records_display(request, panel):

    user_id = request.session.get('user_id')

    if user_id:
        pass
    else:
        return redirect(user_login)

    user = User.objects.get(user_id=user_id)
    office = user.office_id_id

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    selected_documents = request.session.get('selected_documents', [])
    selection = False

    if panel == 'For-ACT-Forwarding':
        documents = Document.objects.filter(status='For SRO Receiving', next_route=office).order_by('-recent_update')
        status = 'For ACT Forwarding'
        selection = True
    elif panel == 'For-Resolving':
        documents = Document.objects.filter(status='For Resolving', next_route=office).order_by('-recent_update')
        status = 'For Resolving'
        selection = True
    elif panel == 'For-ACT-Receiving':
        documents = Document.objects.filter(status='For ACT Receiving', next_route=office).order_by('-recent_update')
        status = 'For ACT Receiving'
    else:
        documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving", "For ACT Receiving"], next_route=office).order_by('-recent_update')
        status = 'SRO All Documents'

    # FILTERING:
    filter_documents = request.session.get('filter_documents')  
    if filter_documents:

        filter_type = filter_documents.get('types', [])
        filter_priority = filter_documents.get('priorities', [])

        if filter_type:
            documents = documents.filter(document_type__category__in=filter_type)
        if filter_priority:
            documents = documents.filter(document_type__priority_level__priority_level__in=filter_priority)

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents_sro(documents, sort_by, order, status, office)

    context = {
        'selected_documents': selected_documents,
        'selection': selection,
        'documents': documents,
        'search_query': search_query,
        'user': 'SRO',
        'today': date.today()
    }

    html = render_to_string('partials/display-records-with-mult-update.html', context)
    return JsonResponse({'html': html})

def action_officer_update_records_display(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect(user_login)

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    selected_documents = request.session.get('selected_documents', [])

    documents = Document.objects.filter(status='For ACT Receiving', act_receiver=user_id).order_by('-recent_update')

    # FILTERING:
    filter_documents = request.session.get('filter_documents')  
    if filter_documents:

        filter_type = filter_documents.get('types', [])
        filter_priority = filter_documents.get('priorities', [])

        if filter_type:
            documents = documents.filter(document_type__category__in=filter_type)
        if filter_priority:
            documents = documents.filter(document_type__priority_level__priority_level__in=filter_priority)

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents_act(documents, sort_by, order, user_id)

    context = {
        'selection': True,
        'selected_documents': selected_documents,
        'documents': documents,
        'search_query': search_query,
        'user': 'ACT',
        'today': date.today()
    }

    html = render_to_string('partials/display-records-with-mult-update.html', context)
    return JsonResponse({'html': html})

def update_reports_display(request, report_type):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect(user_login)

    search_query = request.GET.get('search', '').strip()

    if report_type == 'employee-performance':
        reports = Reports.objects.filter(report_type='Employee Performance', is_active=True)
    elif report_type == 'office-performance':
        reports = Reports.objects.filter(report_type='Office Performance', is_active=True)
    else:
        reports = Reports.objects.filter(is_active=True)
    # Search filter
    if search_query:
        reports = reports.filter(
            Q(report_name__icontains=search_query)
        )

        for report in reports:
            if search_query in report.report_name:
                report.highlighted_report_name = report.report_name.replace(
                    search_query, f"<span class='highlight-search'>{search_query}</span>"
                )
            else:
                report.highlighted_report_name = report.report_name
    
    context = {
        'reports': reports,
        'search_query': search_query
    }

    html = render_to_string('partials/display-reports.html', context)
    return JsonResponse({'html': html})

def update_unacted_records_display(request,):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect(user_login)

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    unacted_logs = UnactedLogs.objects.filter(user_id_id=user_id, is_acted=False)

    if search_query:
        unacted_logs = search_unacted_documents(unacted_logs, search_query)

    context = {
        'unacted_logs': unacted_logs,
        'search_query': search_query,
    }

    html = render_to_string('partials/display-unacted-records.html', context)

    return JsonResponse({'html': html})

def update_archive_display(request, user):

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    documents = Document.objects.filter(status='archived').order_by('-recent_update')

    if search_query:
        documents = search_documents(documents, search_query)

    """if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  
        documents = sort_documents(documents, sort_by, order, "All Records")"""

    context = {
        'documents': documents,
        'search_query': search_query,
        'user': user,
        'today': date.today() 
    }

    html = render_to_string('partials/display-records.html', context)
    return JsonResponse({'html': html})

# ------------------ REPORTS -----------------------

def generate_document_report(request, document_no):

    user_id = request.session.get('user_id')
    user_profile = request.session.get('user_profile', None)
    user_name = user_profile.get('firstname') + ' ' + user_profile.get('lastname')

    if not user_id:
        return redirect(user_login)

    role = user_id.split('-')[0]

    if role == 'SYS':
        role = 'System Admin'
    elif role == 'DIR':
        role = 'Director'
    elif role == 'ADO':
        role = 'Admin Officer'
    elif role == 'SRO':
        role = 'Sub-Receiving Officer'
    else:
        role = 'Action Officer'

    reporter = user_name + ", " + role


    document = Document.objects.get(document_no=document_no)
    logs = ActivityLogs.objects.filter(document_id_id=document_no).order_by('-time_stamp')

    context = {
        'document': document,
        'logs': logs,
        'now': now(),
        'reporter': reporter
    }

    html_string = render_to_string('partials/document-report-pdf.html', context)

    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

    # If there was an error
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Document-Report.pdf"'

    return response

def new_employee_report(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':
        # Extract data from POST request
        report_name = request.POST.get('report_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        employee_id = request.POST.get('target_employee')
        print('target employee: ', employee_id)

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        if end_date_obj < start_date_obj:
            data = {
                'validDates': False
            }
            return JsonResponse(data)

        report = Reports.objects.create(
            report_name=report_name,
            report_type='Employee Performance',
            last_update=timezone.now(),
            start_date=start_date,
            end_date=end_date,
            employee_id=User.objects.get(employee_id=employee_id)
        )
        report.save()

        ReportManagementLogs.objects.create(
            time_stamp = timezone.now(),
            activity='Report Generated',
            report = report,
            user_id=user_id
        )

        data = {
            'validDates': True,
        }
        return JsonResponse(data)

    if role == 'SYS':
        return redirect(system_admin_performance_reports)
    elif role == 'DIR':
        return redirect(director_performance_reports)

def new_office_report(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if not user_id:
        return redirect('user_login')
    
    if request.method == 'POST':
        # Extract data from POST request
        report_name = request.POST.get('report_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        office_id = request.POST.get('office')

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        if end_date_obj < start_date_obj:
            data = {
                'validDates': False
            }
            return JsonResponse(data)
        
        report = Reports.objects.create(
            report_name=report_name,
            report_type='Office Performance',
            last_update=timezone.now(),
            start_date=start_date,
            end_date=end_date,
            office_id_id=office_id
        )
        report.save()

        ReportManagementLogs.objects.create(
            time_stamp = timezone.now(),
            activity='Report Generated',
            report = report,
            user_id=user_id
        )
 
        data = {
            'validDates': True
        }
        return JsonResponse(data)

    if role == 'SYS':
        return redirect(system_admin_performance_reports)
    elif role == 'DIR':
        return redirect(director_performance_reports)

def delete_report(request, report_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)

    report = Reports.objects.get(report_no=report_no)
    report.is_active = False
    report.save()

    ReportManagementLogs.objects.create(
        time_stamp = timezone.now(),
        activity='Report Deleted',
        report = report,
        user_id=user_id
    )

    data = {
        'message': f'Report {report_no} has been successfully deleted.'
    }
    return JsonResponse(data)

def load_target_employees(request):

    selected_employee_office = request.GET.get('selected_employee_office')
    users = User.objects.filter(status='active', office_id_id=selected_employee_office).values(
        'employee_id', 'firstname', 'lastname'
    ).order_by('lastname')
    return JsonResponse(list(users), safe=False)

def download_performance_report(request, report_no):

    user_id = request.session.get('user_id')
    user_profile = request.session.get('user_profile', None)
    user_name = user_profile.get('firstname') + ' ' + user_profile.get('lastname')
    if not user_id:
        return redirect(user_login)

    role = user_id.split('-')[0]

    if role == 'SYS':
        role = 'System Admin'
    elif role == 'DIR':
        role = 'Director'
    elif role == 'ADO':
        role = 'Admin Officer'
    elif role == 'SRO':
        role = 'Sub-Receiving Officer'
    else:
        role = 'Action Officer'

    reporter = user_name + ", " + role

    report = Reports.objects.get(report_no=report_no)
    converted_start_date = datetime.combine(report.start_date, time.min)
    converted_end_date = datetime.combine(report.end_date, time.max)
    converted_start_date = timezone.make_aware(converted_start_date)
    converted_end_date = timezone.make_aware(converted_end_date)

    if report.report_type == 'Employee Performance':

        endorsed_documents_count = 0
        action_officer_total_received_documents = 0
        approved_documents_count = 0
        director_total_received_documents = 0
        sro_received_documents_count = 0
        delayed_documents = []
        delayed_forwarding_documents = []
        delayed_resolving_documents = []
        resolved_documents_count = 0
        created_documents_count = 0
        routed_documents_count = 0
        
        middlename = report.employee_id.middlename

        if middlename:
            middlename = middlename[0].title() + ". "
        else:
            middlename = ''

        name = report.employee_id.firstname.title() + " " + middlename + report.employee_id.lastname

        role = report.employee_id.role

        if role == 'ADO':
            position = 'Admin Officer'
            routed_documents_count = ActivityLogs.objects.filter(
                activity='Document Routed',
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count
            created_documents_count = ActivityLogs.objects.filter(
                activity='Document Created',
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count

        elif role == 'Director':    
            position = 'Director'
            approved_documents_count = ActivityLogs.objects.filter(
                activity='Document Approved',
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count
            director_total_received_documents = ActivityLogs.objects.filter(
                activity='Document Created',
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()
            director_total_received_documents += ActivityLogs.objects.filter(
                activity='Document Resolved',
                receiver_id_id='DIR-1001',
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()

        elif role == 'SRO':
            position = 'Sub-receiving Officer'

            resolved_documents_count = ActivityLogs.objects.filter(
                activity='Document Resolved',
                user_id = report.employee_id,
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()

            sro_received_documents_count = ActivityLogs.objects.filter(
                activity='Document Resolved',
                receiver_id = report.employee_id,
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()

            print("received docs count", sro_received_documents_count)

            delayed_forwarding_documents = UnactedLogs.objects.filter(
                user_id_id = report.employee_id_id,
                is_acted=True,
                status='For SRO Receiving',
                date_acted__range=[report.start_date, report.end_date]
            )

            for docu in delayed_forwarding_documents: 
                tracking_no_parts = docu.document_id.tracking_no.split('-', 1)
                docu.tracking_no_first = tracking_no_parts[0]  
                docu.tracking_no_second = tracking_no_parts[1]
                docu.delayed_days = (docu.date_acted - docu.time_stamp).days

            delayed_resolving_documents = UnactedLogs.objects.filter(
                user_id_id = report.employee_id_id,
                is_acted=True,
                status='For Resolving',
                date_acted__range=[report.start_date, report.end_date]
            )

            for docu in delayed_resolving_documents: 
                tracking_no_parts = docu.document_id.tracking_no.split('-', 1)
                docu.tracking_no_first = tracking_no_parts[0]  
                docu.tracking_no_second = tracking_no_parts[1]
                docu.delayed_days = (docu.date_acted - docu.time_stamp).days

        else:
            position = 'Action Officer'

            endorsed_documents_count = ActivityLogs.objects.filter(
                activity='Document Endorsed by Action Officer', 
                user_id_id=report.employee_id_id, 
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()
            action_officer_total_received_documents = ActivityLogs.objects.filter(
                activity='Document Forwarded to Action Officer',
                receiver_id = report.employee_id,
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()
            action_officer_total_received_documents += ActivityLogs.objects.filter(
                activity='Document Reassigned Due to Inaction',
                receiver_id=report.employee_id,
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()
        
        if role != 'ACT':
            delayed_documents = UnactedLogs.objects.filter(
                user_id_id = report.employee_id_id,
                is_acted=True,
                date_acted__range=[report.start_date, report.end_date]
            )

            for docu in delayed_documents: 
                tracking_no_parts = docu.document_id.tracking_no.split('-', 1)
                docu.tracking_no_first = tracking_no_parts[0]  
                docu.tracking_no_second = tracking_no_parts[1]
                docu.delayed_days = (docu.date_acted - docu.time_stamp).days

        unacted_logs = UnactedLogs.objects.filter(
            user_id_id = report.employee_id_id,
            is_acted=False,
            time_stamp__range=[converted_start_date, converted_end_date]
        )

        for log in unacted_logs: 
            tracking_no_parts = log.document_id.tracking_no.split('-', 1)
            log.tracking_no_first = tracking_no_parts[0]  
            log.tracking_no_second = tracking_no_parts[1]
            
        context = {
            'reporter': reporter,
            'report': report,
            'name': name,
            'now': now(),
            'position': position,
            'endorsed_documents_count': endorsed_documents_count,
            'action_officer_total_received_documents': action_officer_total_received_documents,
            'approved_documents_count': approved_documents_count,
            'director_total_received_documents': director_total_received_documents,
            'resolved_documents_count': resolved_documents_count,
            'sro_received_documents_count': sro_received_documents_count,
            'delayed_documents': delayed_documents,
            'delayed_forwarding_documents': delayed_forwarding_documents,
            'delayed_resolving_documents': delayed_resolving_documents,
            'routed_documents_count': routed_documents_count,
            'created_documents_count': created_documents_count,
            'unacted_logs': unacted_logs
        }

        html_string = render_to_string('partials/employee-performance-report.html', context)

    else:

        sro = User.objects.get(status='active', office_id_id=report.office_id_id, role='SRO')
        middlename = sro.middlename

        if middlename:
            middlename = middlename[0].title() + ". "
        else:
            middlename = ''

        name = sro.firstname.title() + " " + middlename + sro.lastname
        no_of_employees = User.objects.filter(status='active', role='ACT', office_id_id=report.office_id_id).count()
        print("user id: ", sro.user_id)
        received_documents_count = ActivityLogs.objects.filter(
            activity='Document Routed', 
            receiver_id=sro,
            time_stamp__range=[converted_start_date, converted_end_date]
            ).count()

        resolved_documents_count = ActivityLogs.objects.filter(
            activity='Document Resolved', 
            user_id__office_id__office_id = sro.office_id_id,
            time_stamp__range=[converted_start_date, converted_end_date]
            ).count()

        delayed_logs = UnactedLogs.objects.filter(
            user_id__role__in=['SRO', 'ACT'],
            is_acted=True,
            time_stamp__range=[converted_start_date, converted_end_date]
        )

        for docu in delayed_logs: 
                tracking_no_parts = docu.document_id.tracking_no.split('-', 1)
                docu.tracking_no_first = tracking_no_parts[0]  
                docu.tracking_no_second = tracking_no_parts[1]
                docu.delayed_days = (docu.date_acted - docu.time_stamp).days

        unacted_logs = UnactedLogs.objects.filter(
            user_id__role__in=['SRO', 'ACT'],
            is_acted=False,
            time_stamp__range=[converted_start_date, converted_end_date]
        )

        for log in unacted_logs: 
            tracking_no_parts = log.document_id.tracking_no.split('-', 1)
            log.tracking_no_first = tracking_no_parts[0]  
            log.tracking_no_second = tracking_no_parts[1]

        context = {
            'reporter': reporter,
            'now': now(),
            'name': name,
            'no_of_employees': no_of_employees,
            'report': report,
            'received_documents_count': received_documents_count,
            'resolved_documents_count': resolved_documents_count,
            'unacted_logs': unacted_logs,
            'delayed_logs': delayed_logs,
        }

        html_string = render_to_string('partials/office-performance-report.html', context)

    
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Performance-Report.pdf"'

    return response

def generate_pending_report(request, target_user_id):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)

    user_profile = request.session.get('user_profile', None)
    user_name = user_profile.get('firstname') + ' ' + user_profile.get('lastname')

    role = user_id.split('-')[0]

    if role == 'SYS':
        role = 'System Admin'
    elif role == 'DIR':
        role = 'Director'
    elif role == 'ADO':
        role = 'Admin Officer'
    elif role == 'SRO':
        role = 'Sub-Receiving Officer'
    else:
        role = 'Action Officer'

    reporter = user_name + ", " + role

    target_user = User.objects.get(user_id=target_user_id)

    if target_user.role == 'ADO':
        pending_documents = Document.objects.filter(status='For Routing').order_by('-recent_update')
    elif target_user.role == 'SRO':
        pending_documents = Document.objects.filter(
            status='For SRO Receiving', 
            next_route=target_user.office_id_id
        ).order_by('-recent_update')
    elif target_user.role == 'ACT':
        pending_documents = Document.objects.filter(
            status='For ACT Receiving',
            act_receiver=target_user_id
        ).order_by('-recent_update')

    context = {
        'target_user': target_user,
        'now': now(),
        'pending_documents': pending_documents,
        'reporter': reporter
    }

    html_string = render_to_string('partials/pending-documents-report.html', context)

    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Pending-Document-Report.pdf"'

    return response

# ------------------ REMARKS -----------------------
import difflib
DICTIONARY = ['prioritize', 'priority', 'urgent', 'emergency', 'urgency', 'immediately', 'immediate', 'need', 'soonest', 'asap', 'as soon as possible', 'very urgent']

def highlight_words(remarks, detected_words):
    for original_word, match in detected_words.items():
        # Use the original word or the close match for highlighting
        remarks = remarks.replace(original_word, f"<span style='color: red;'>{match}</span>")
    return remarks

def is_high_priority(remarks):
    remarks_words = remarks.lower().split()
    detected_words = {}

    for word in remarks_words:
        # Check if the word is in the dictionary or if there's a close match
        if word in DICTIONARY:
            detected_words[word] = word  # Exact match
        else:
            close_match = difflib.get_close_matches(word, DICTIONARY, n=1, cutoff=0.8)
            if close_match:
                detected_words[word] = close_match[0]  # Close match found

    return detected_words if detected_words else None

def check_remarks(request, document_no, activity_log_no):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':

        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')
        activity_log = ActivityLogs.objects.get(no=activity_log_no)

        detected_words = is_high_priority(remarks)

        if detected_words:

            high_priority_detected = True
            highlighted_remarks = highlight_words(remarks, detected_words)
            
            document = Document.objects.get(document_no=document_no)
            prio_level = document.document_type.priority_level.priority_level

            if prio_level == 'very urgent':

                high_priority_detected = False
                document.remarks = remarks
                document.save()

                if file_attachment:
                    folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(document_no))
                    file_attachment = handle_file_versioning(file_attachment, folder_path)
                    activity_log.file_attachment = file_attachment
                    activity_log.save()

                new_remarks = Remarks.objects.get(no=activity_log.remarks.no)
                new_remarks.remarks = remarks
                new_remarks.save()

        else:

            high_priority_detected = False
            highlighted_remarks = remarks  # No highlights if no priority words
            
            editRemarks = Remarks.objects.get(no=activity_log.remarks.no)
            editRemarks.remarks = remarks
            editRemarks.save()
            
            if file_attachment:
                folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(document_no))
                file_attachment = handle_file_versioning(file_attachment, folder_path)
                activity_log.file_attachment = file_attachment
                activity_log.save()

            document = Document.objects.get(document_no=document_no)
            document.remarks = remarks
            document.save()
    
    data = {
        'remarks': remarks,
        'high_priority_detected': high_priority_detected,
        'highlighted_remarks': highlighted_remarks
    }

    return JsonResponse(data)

from django.core.files.base import ContentFile

def multiple_update_remarks(request, remarks_no):

    if request.method == 'POST':

        activity_logs_no = request.POST.getlist('activityLogsNo')
        activity_logs_no = ast.literal_eval(activity_logs_no[0])
        documents_no = request.POST.get('checkedValues')
        documents_no = json.loads(documents_no)
        documents_no = list(map(int, documents_no))
        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')

        detected_words = is_high_priority(remarks)

        if detected_words:

            high_priority_detected = True
            highlighted_remarks = highlight_words(remarks, detected_words)

            documents = Document.objects.filter(document_no__in=documents_no)
            
            documents_to_prioritize = []

            for document in documents:

                if document.document_type.priority_level.priority_level != 'very urgent':

                    documents_to_prioritize.append(document.document_no)

            if not documents_to_prioritize:

                high_priority_detected = False

                for document in documents:

                    document.remarks = remarks
                    document.save()
                
                logs = ActivityLogs.objects.filter(no__in=activity_logs_no)

                logs.update(remarks_id=remarks_no)

                if file_attachment:
                    for log in logs:
                        folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(log.document_id.document_no))
                        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
                        file_attachment_name = handle_file_versioning(file_attachment, folder_path)
                        with open(file_attachment.temporary_file_path(), 'rb') as f:
                            file_content = f.read()
                        
                        log.file_attachment.save(file_attachment_name, ContentFile(file_content))
                        log.save()

                remarks_instance = Remarks.objects.get(no=remarks_no)
                remarks_instance.remarks = remarks
                remarks_instance.save()
            
            else:
                high_priority_detected = True

        else:

            high_priority_detected = False
            highlighted_remarks = ""

            documents = Document.objects.filter(document_no__in=documents_no)

            for document in documents:
                document.remarks = remarks
                document.save()

            logs = ActivityLogs.objects.filter(no__in=activity_logs_no)

            logs.update(remarks_id=remarks_no)

            if file_attachment:
                for log in logs:
                    folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(log.document_id.document_no))
                    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
                    file_attachment_name = handle_file_versioning(file_attachment, folder_path)
                    with open(file_attachment.temporary_file_path(), 'rb') as f:
                        file_content = f.read()
                    
                    log.file_attachment.save(file_attachment_name, ContentFile(file_content))
                    log.save()

            remarks_instance = Remarks.objects.get(no=remarks_no)
            remarks_instance.remarks = remarks
            remarks_instance.save()

    data = {
        "high_priority_detected": high_priority_detected,
        'highlighted_remarks': highlighted_remarks,
    }

    return JsonResponse(data)

def multiple_update_reject_remarks(request, remarks_no):

    if request.method == 'POST':

        activity_logs_no = request.POST.getlist('activityLogsNo')
        activity_logs_no = ast.literal_eval(activity_logs_no[0])

        documents_no = request.POST.get('checkedValues')
        documents_no = json.loads(documents_no)
        documents_no = list(map(int, documents_no))

        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')

        documents = Document.objects.filter(document_no__in=documents_no)

        for document in documents:
            document.remarks = remarks
            document.save()

        logs = ActivityLogs.objects.filter(no__in=activity_logs_no)

        logs.update(remarks_id=remarks_no)

        if file_attachment:
                for log in logs:
                    folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(log.document_id.document_no))
                    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
                    file_attachment_name = handle_file_versioning(file_attachment, folder_path)
                    with open(file_attachment.temporary_file_path(), 'rb') as f:
                        file_content = f.read()
                    
                    log.file_attachment.save(file_attachment_name, ContentFile(file_content))
                    log.save()

        remarks_instance = Remarks.objects.get(no=remarks_no)
        remarks_instance.remarks = remarks
        remarks_instance.save()

    data = {
        'success': 'success'
    }

    return JsonResponse(data)

def change_priority_level(request, document_no, activity_log_no):

    if request.method == 'POST':

        activity_log = ActivityLogs.objects.get(no=activity_log_no)

        remarks = request.POST.get('remarks')
        file_attachment = request.FILES.get('attachment')

        new_remarks = Remarks.objects.get(no=activity_log.remarks.no)
        new_remarks.remarks = remarks
        new_remarks.save()

        document = Document.objects.get(document_no=document_no)
        
        new_document_type = DocumentType.objects.create(
            document_type=document.document_type.document_type,
            category=document.document_type.category,
            priority_level_id=3,
            is_active = False
        )

        current_routes = DocumentRoute.objects.filter(
            document_type=document.document_type
        )

        for route_instance in current_routes:
            DocumentRoute.objects.create(
                document_type = new_document_type,
                route_id = route_instance.route_id
            )

        document.old_document_type = document.document_type.document_no
        document.document_type = new_document_type
        document.remarks = remarks
        document.save()

        if file_attachment:
            folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(document_no))
            file_attachment = handle_file_versioning(file_attachment, folder_path)
            activity_log.file_attachment = file_attachment
            activity_log.save()

        data = {
            'sucess': 'sucess'
        }
        return JsonResponse(data)

import ast
def change_priority_level_multiple_documents(request):

    if request.method == 'POST':

        remarks_no = request.POST.get('remarks_no')
        activity_logs_no = request.POST.getlist('activity_logs_no') 
        activity_logs_no = ast.literal_eval(activity_logs_no[0])
        checked_values = request.POST.get('checked_values')
        checked_values = json.loads(checked_values)
        checked_values = list(map(int, checked_values))

        remarks = request.POST.get('remarks')

        attachment = request.FILES.get('attachment') 

        documents = Document.objects.filter(document_no__in=checked_values)

        logs = ActivityLogs.objects.filter(no__in=activity_logs_no)


        for document in documents:

            document_prio_level = document.document_type.priority_level.priority_level

            if document_prio_level != "very urgent":

                new_document_type = DocumentType.objects.create(
                    document_type=document.document_type.document_type,
                    category=document.document_type.category,
                    priority_level_id=3,
                    is_active = False
                )

                current_routes = DocumentRoute.objects.filter(
                    document_type=document.document_type
                )

                for route_instance in current_routes:
                    DocumentRoute.objects.create(
                        document_type = new_document_type,
                        route_id = route_instance.route_id
                    )
                
                document.old_document_type = document.document_type.document_no
                document.document_type = new_document_type
    

            document.remarks = remarks
            document.save()
        
        logs.update(remarks_id=remarks_no)

        if attachment:
            for log in logs:
                folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(log.document_id.document_no))
                os.makedirs(folder_path, exist_ok=True)
                file_attachment_name = handle_file_versioning(attachment, folder_path)
                with open(attachment.temporary_file_path(), 'rb') as f:
                    file_content = f.read()
                
                log.file_attachment.save(file_attachment_name, ContentFile(file_content))
                log.save()

        remarks_instance = Remarks.objects.get(no=remarks_no)
        remarks_instance.remarks = remarks
        remarks_instance.save()

    data = {
        "sucess": "success"
    }

    return JsonResponse(data)

def handle_file_versioning(file, folder_path):
    # Start with the original name and extension
    original_name, extension = os.path.splitext(file.name)
    version = 1
    
    # Sanitize the filename by removing spaces and any unwanted characters
    base_name = original_name.replace(' ', '_').replace('(', '').replace(')', '')

    # Generate the initial file name
    new_file_name = f"{base_name}{extension}"

    # Loop to check if the file already exists
    while os.path.exists(os.path.join(folder_path, new_file_name)):
        # Increment the version and create a new file name with "-v{version}"
        version += 1
        new_file_name = f"{base_name}-v{version}{extension}"

    # Rename the file with the final versioned name
    file.name = new_file_name
    return file

def generate_upload_file_qrcode(request, activity_log_no):
    print("pumasok sa generate upload file qr code views")
    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    
    url = request.build_absolute_uri(f'/upload-file-page/{activity_log_no}/')

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(color="black", back_color='white')

    # Save to a BytesIO buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type='image/png')

def upload_file_page(request, activity_log_no):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    try:
        activity_log = ActivityLogs.objects.get(no=activity_log_no)
    except ActivityLogs.DoesNotExist:
        return render(request, "upload-file-error-page.html", {'invalidUrl': True})

    if user_id == activity_log.user_id_id:
        if activity_log.file_attachment:
            return render(request, "upload-file-error-page.html", {'fileUploaded': True})
        else:
            return render(request, "upload-file-page.html", {'activity_log_no':activity_log_no})
    else:
        return render(request, "upload-file-error-page.html", {'unauthorized': True})

def upload_file_with_phone(request, activity_log_no):

    if request.method == 'POST':
        file_attachment = request.FILES.get('attachment')
        activity_log = ActivityLogs.objects.get(no=activity_log_no)
        folder_path = os.path.join(settings.MEDIA_ROOT, "document", str(activity_log.document_id.document_no))
        file_attachment = handle_file_versioning(file_attachment, folder_path)
        activity_log.file_attachment = file_attachment
        activity_log.save()

    return redirect(reverse('upload_file_page', args=[activity_log_no]))

from os.path import basename

def fetch_phone_upload_file(request, activity_log_no):

    activity_log = ActivityLogs.objects.get(no=activity_log_no)

    if activity_log.file_attachment:

        filename = basename(activity_log.file_attachment.name)
        print(filename)
        data = {
            'filename': filename
        }
        return JsonResponse(data)
    
    data = {
        'filename': False
    }
    return JsonResponse(data)


def delete_phone_upload_file(request, activity_log_no):

    activity_log = ActivityLogs.objects.get(no=activity_log_no)
    activity_log.file_attachment = None
    activity_log.save()
    return JsonResponse({'data': 'sucess'})# ------------------ USER PROFILE -----------------------

def edit_profile(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':

        new_profile_photo = request.FILES.get('new_profile_photo')
        new_firstname = request.POST.get('new_firstname')
        new_middlename = request.POST.get('new_middlename')
        new_lastname = request.POST.get('new_lastname')
        new_contact_no = request.POST.get('new_contact_no')
        temp_delete_profile = request.POST.get('temp_delete_profile')

        user = User.objects.get(user_id=user_id)
        current_profile_photo = user.profile_picture.name

        user.firstname = new_firstname.title()
        if new_middlename:
            user.middlename = new_middlename.title()
        else:
            user.middlename = ""
        user.lastname = new_lastname.title()
        user.contact_no = new_contact_no

        if new_profile_photo and current_profile_photo:
            profile_picture_path = os.path.join(settings.MEDIA_ROOT, str(current_profile_photo))
            if os.path.exists(profile_picture_path):
                os.remove(profile_picture_path)
            user.profile_picture = new_profile_photo

        else:

            if not new_profile_photo and current_profile_photo:
                pass
            else:
                user.profile_picture = new_profile_photo

            if not new_profile_photo and current_profile_photo and temp_delete_profile == 'yes':
                # Delete the current profile picture file
                profile_picture_path = os.path.join(settings.MEDIA_ROOT, str(current_profile_photo))
                if os.path.exists(profile_picture_path):
                    os.remove(profile_picture_path)
                user.profile_picture = new_profile_photo
            
        user.save()

        del request.session['user_profile']

        if user.role == 'ADO':
            role='Admin Officer'
        elif user.role == 'SRO':
            role = 'Sub-receiving Officer'
        elif user.role == 'ACT':
            role = 'Action Officer'
        elif user.role == 'Director':
            role = 'Director'
        elif user.role == 'System Admin':
            role = 'System Administrator'

        user_profile = {
            'user_id': user.user_id,
            'role': role,
            'firstname': user.firstname.title(),
            'middlename': user.middlename.title(),
            'lastname': user.lastname.title(),
            'email': user.email,
            'contact_no': user.contact_no,
            'profile_picture': user.profile_picture.name
        }
        
        request.session['user_profile'] = user_profile

    return JsonResponse({'status': 'success'})

def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')  # Redirect if not logged in
    
    # Get the user from the database using the user_id from the session
    user = get_object_or_404(User, user_id=user_id)
    
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        
        if form.is_valid():
            # Update user's password directly, as per your request
            new_password = form.cleaned_data['new_password']
            user.password = new_password  # Direct assignment of the new password
            user.save()

            # Update session data (if needed)
            request.session['user_profile'] = {
                'user_id': user.user_id,
                'role': user.role,
                'firstname': user.firstname.title(),
                'middlename': user.middlename.title() if user.middlename else "",
                'lastname': user.lastname.title(),
                'email': user.email,
                'contact_no': user.contact_no,
                'profile_picture': user.profile_picture.name
            }

            return JsonResponse({
                'status': 'success',
                'icon': 'success',
                'title': 'Password Changed',
                'message': 'Your password has been updated successfully!',
                'background_color': '#d4edda'
            })

        # Return form errors as JSON if the form is invalid
        errors = form.errors.as_json()
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'title': 'Password Change Failed',
            'message': 'There were some issues with your submission. Please double check your input.',
            'background_color': '#f8d7da',
            'errors': errors
        })

    # Invalid request type
    return JsonResponse({
        'status': 'invalid_request',
        'icon': 'info',
        'title': 'Invalid Request',
        'message': 'Only POST requests are allowed for this operation.',
        'background_color': '#fff3cd'
    }, status=400)


# ------------------ ANNOUNCEMENTS -----------------------

def update_announcement(request, id):
    if request.method == 'POST':
        try:
            announcement = Announcement.objects.get(id=id)
        except Announcement.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Announcement not found.'}, status=404)

        # Accessing the title directly
        title = announcement.title  # Directly getting the title from the database
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def delete_announcement(request, id):
    if request.method == 'POST':
        try:
            announcement = get_object_or_404(Announcement, id=id)
            announcement.delete()
            return JsonResponse({'status': 'success'})
        except Announcement.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Announcement not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def view_attachment(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # Serve the converted PDF if available
    if announcement.attachment:
        pdf_name = os.path.splitext(announcement.attachment.name)[0] + '.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='application/pdf')
        else:
            return HttpResponse("PDF conversion not available.", status=404)
    return HttpResponse("No attachment", status=404)

# ------------------ ANALYTICS -----------------------

def system_admin_user_application_analytics(request):

    users = User.objects.all()

    pending_count = users.filter(status='for verification').count()
    active_count = users.filter(status='active').count()
    inactive_count = users.filter(status='inactive').count()

    data = {
        'pending_count': pending_count,
        'active_count': active_count,
        'inactive_count': inactive_count
    }

    return JsonResponse(data)

def director_total_records(request, time_span):

    start_date, end_date = get_time_span(time_span)

    records = Document.objects.filter(recent_update__gte=start_date, recent_update__lt=end_date)

    director_total_records = records.filter(status='For DIR Approval').count()
    adm_total_records = records.filter(status__in=['For Routing', 'For Archiving', 'Rejected']).count()
    csr_total_records = records.filter(status__in=['For SRO Receiving', 'For ACT Receiving', 'For Resolving'], next_route='CSR').count()
    bdm_total_records = records.filter(status__in=['For SRO Receiving', 'For ACT Receiving', 'For Resolving'], next_route='BMD').count()
    acc_total_records = records.filter(status__in=['For SRO Receiving', 'For ACT Receiving', 'For Resolving'], next_route='ACC').count()
    prl_total_records = records.filter(status__in=['For SRO Receiving', 'For ACT Receiving', 'For Resolving'], next_route='PRL').count()

    overall_total_records = (
        director_total_records +
        adm_total_records +
        csr_total_records +
        bdm_total_records +
        acc_total_records +
        prl_total_records
    )

    data = {
        'overall_total_records': overall_total_records,
        'director_total_records': director_total_records,
        'adm_total_records': adm_total_records,
        'csr_total_records': csr_total_records,
        'bdm_total_records': bdm_total_records,
        'acc_total_records': acc_total_records,
        'prl_total_records': prl_total_records
    }

    return JsonResponse(data)

def director_document_status(request, time_span, document_status):

    start_date, end_date = get_time_span(time_span)

    if document_status == 'all-documents':
        records = Document.objects.filter(
            recent_update__gte=start_date, 
            recent_update__lt=end_date
        ).exclude(status__in=['Archived', 'Rejected'])
    else:
        records = Document.objects.filter(recent_update__gte=start_date, recent_update__lt=end_date, status=document_status)

    very_urgent = records.filter(document_type__priority_level__priority_level = 'very urgent').count()
    urgent = records.filter(document_type__priority_level__priority_level = 'urgent').count()
    normal = records.filter(document_type__priority_level__priority_level = 'normal').count()
    for_pref_action = records.filter(document_type__priority_level__priority_level = 'for pref. action').count()

    data = {
        'very_urgent': very_urgent,
        'urgent': urgent,
        'normal': normal,
        'for_pref_action': for_pref_action
    }

    return JsonResponse(data)

def director_office_performance(request, time_span, target_office):

    start_date, end_date = get_time_span(time_span)

    unacted = UnactedLogs.objects.filter(
        user_id__office_id__office_id=target_office,
        is_acted=False,
        time_stamp__gte=start_date, 
        time_stamp__lt=end_date
    ).count()

    now = timezone.localtime().date()

    if target_office == 'DIR':
        status = 'For DIR Approval'
    elif target_office == 'ADM':
        status = 'For Routing'
    else:
        status = ['For SRO Receiving', 'For ACT Receiving', 'For Resolving']
    
    if target_office in ['DIR', 'ADM']:

        pending = Document.objects.filter(
            status=status,
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            ongoing_deadline__gt=now
        ).count()

    else:
        pending = Document.objects.filter(
            status__in=status,
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            ongoing_deadline__gt=now,
            next_route=target_office
        ).count()

    delayed = UnactedLogs.objects.filter(
        user_id__office_id__office_id=target_office,
        is_acted=True,
        time_stamp__gte=start_date, 
        time_stamp__lt=end_date
    ).count()

    if target_office in ['ACC', 'BMD', 'CSR', 'PRL']:

        resolved = ActivityLogs.objects.filter(
            user_id__office_id__office_id=target_office,
            activity = 'Document Resolved',
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date
        ).count()

        data = {
            'target_office': target_office,
            'unacted': unacted,
            'pending': pending,
            'delayed': delayed,
            'resolved': resolved
        }
        return JsonResponse(data)
    data = {
        'target_office': target_office,
        'unacted': unacted,
        'pending': pending,
        'delayed': delayed
    }
    return JsonResponse(data)

def director_employee_performance(request, time_span, target_report_type, target_office):

    start_date, end_date = get_time_span(time_span)
    now = timezone.localtime().date()

    if target_office == 'All Offices':
        employees = User.objects.filter(status='active').exclude(role='System Admin')
    else:
        employees = User.objects.filter(status='active', office_id_id=target_office).exclude(role='System Admin')

    performances = {}

    for emp in employees:
            
        if emp.role == 'Director':
            acted_document_count = ActivityLogs.objects.filter(
                activity = 'Document Approved',
                time_stamp__gte=start_date, 
                time_stamp__lt=end_date
            ).count()

            pending_document_count = Document.objects.filter(
                status='For DIR Approval',
                recent_update__gte=start_date,
                ongoing_deadline__gt=now
            ).count()

        elif emp.role == 'ADO':
            acted_document_count = ActivityLogs.objects.filter(
                activity = 'Document Routed',
                time_stamp__gte=start_date, 
                time_stamp__lt=end_date
            ).count()

            pending_document_count = Document.objects.filter(
                status='For Routing',
                recent_update__gte=start_date,
                ongoing_deadline__gt=now
            ).count()

        elif emp.role == 'SRO':
            acted_document_count = ActivityLogs.objects.filter(
                user_id_id=emp.user_id,
                activity__in=['Document Forwarded to Action Officer', 'Document Resolved'],
                time_stamp__gte=start_date, 
                time_stamp__lt=end_date
            ).count()

            pending_document_count = Document.objects.filter(
                next_route=emp.office_id_id,
                status__in=['For SRO Receiving', 'For Resolving'],
                recent_update__gte=start_date,
                ongoing_deadline__gt=now
            ).count()

        elif emp.role == 'ACT':
            acted_document_count = ActivityLogs.objects.filter(
                user_id_id=emp.user_id,
                activity__in=['Document Endorsed by Action Officer', 'Document Resolved'],
                time_stamp__gte=start_date, 
                time_stamp__lt=end_date
            ).count()

            pending_document_count = Document.objects.filter(
                act_receiver=emp.user_id,
                status='For ACT Receiving',
                recent_update__gte=start_date,
                ongoing_deadline__gt=now
            ).count()
            
        unacted_document_count = UnactedLogs.objects.filter(
            user_id_id=emp.user_id,
            is_acted=False,
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date
        ).count()

        if emp.role in ['ADO', 'SRO', 'Director']:

            pending_document_count += unacted_document_count
            acted_document_count += UnactedLogs.objects.filter(
                user_id_id=emp.user_id,
                is_acted=True,
                time_stamp__gte=start_date, 
                time_stamp__lt=end_date
            ).count()

        total_received_document = acted_document_count + pending_document_count + unacted_document_count

        if total_received_document <= 0:
            average_perf_level = -1
        else:
            if target_report_type == 'Top-Employees':
                average_perf_level = (
                    ((acted_document_count/total_received_document) * 1.0) + 
                    ((pending_document_count/total_received_document) * 0.5) - 
                    ((unacted_document_count/total_received_document) * 0.5) 
                ) * 100
            else:
                average_perf_level = (
                    ((unacted_document_count/total_received_document) * 1.0) +
                    ((pending_document_count/total_received_document) * 0.5)
                ) * 100

        performances[emp.employee_id] = average_perf_level

    filtered_performances = {emp_id: perf for emp_id, perf in performances.items() if perf != -1}
    sorted_performances = dict(sorted(filtered_performances.items(), key=lambda item: item[1])[:10])
    
    data = {
        'target_report_type': target_report_type,
        'sorted_performances': sorted_performances
    }

    return JsonResponse(data)

def get_time_span(time_span):
    
    now = timezone.now()
    if time_span == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return start_date, end_date
    
    elif time_span == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1)
        return start_date, end_date
    
    elif time_span == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date.replace(year=start_date.year + 1)
        return start_date, end_date

def generate_document_status_report(request, time_span, document_status):

    user_profile = request.session.get('user_profile', None)
    user_name = user_profile.get('firstname') + ' ' + user_profile.get('lastname')

    start_date, end_date = get_time_span(time_span)

    if document_status == 'all-documents':

        documents = Document.objects.filter(
            status__in = ['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For ACT Receiving', 'For Resolving', 'For Archiving'],
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
        )

        documents = documents.annotate(
            priority_order=Case(
                When(document_type__priority_level__priority_level="very urgent", then=1),
                When(document_type__priority_level__priority_level="urgent", then=2),
                When(document_type__priority_level__priority_level="normal", then=3),
                default=4,
                output_field=IntegerField(),
            )
        )
        
        for_dir_approval = documents.filter(status='For DIR Approval').order_by('priority_order')
        for_routing = documents.filter(status='For Routing').order_by('priority_order')
        for_sro_receiving = documents.filter(status='For SRO Receiving').order_by('priority_order')
        for_act_receiving = documents.filter(status='For ACT Receiving').order_by('priority_order')
        for_resolving = documents.filter(status='For Resolving').order_by('priority_order')
        for_archiving = documents.filter(status='For Archiving').order_by('priority_order')

        context = {
            'document_status': document_status,
            'now': now(),
            'today': date.today(),
            'for_dir_approval': for_dir_approval,
            'for_routing': for_routing,
            'for_sro_receiving': for_sro_receiving,
            'for_act_receiving': for_act_receiving,
            'for_resolving': for_resolving,
            'for_archiving': for_archiving,
            'user_name': user_name
        }

        html_string = render_to_string('partials/document-status-report.html', context)

    else:

        documents = Document.objects.filter(
            status=document_status,
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
        ).annotate(
            priority_order=Case(
                When(document_type__priority_level__priority_level="very urgent", then=1),
                When(document_type__priority_level__priority_level="urgent", then=2),
                When(document_type__priority_level__priority_level="normal", then=3),
                default=4,
                output_field=IntegerField(),
            )
        ).order_by('priority_order')

        context = {
            'document_status': document_status,
            'now': now(),
            'today': date.today(),
            'documents': documents,
            'user_name': user_name
        }

        html_string = render_to_string('partials/document-status-report.html', context)
        
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Document-Status-Report.pdf"'

    return response

def admin_officer_total_records(request, time_span, target_prio_level):

    start_date, end_date = get_time_span(time_span)

    if target_prio_level == 'all':
        records = Document.objects.filter(
            status__in = ['For DIR Approval', 'For Routing', 'For Archiving'],
            recent_update__gte=start_date, 
            recent_update__lt=end_date
        )
    else:
        records = Document.objects.filter(
            status__in = ['For DIR Approval', 'For Routing', 'For Archiving'],
            document_type__priority_level__priority_level = target_prio_level,
            recent_update__gte=start_date, 
            recent_update__lt=end_date
        )
    
    data = {
        'dir_approval': records.filter(status='For DIR Approval').count(),
        'routing': records.filter(status='For Routing').count(),
        'archiving': records.filter(status='For Archiving').count()
    }

    return JsonResponse(data)

def admin_officer_performance(request, time_span):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    start_date, end_date = get_time_span(time_span)

    resolved_count = ActivityLogs.objects.filter(
        time_stamp__gte=start_date, 
        time_stamp__lt=end_date,
        activity='Document Routed'
    ).count()

    pending_count = Document.objects.filter(
        recent_update__gte=start_date, 
        recent_update__lt=end_date,
        status='For Routing'
    ).count()

    unactedlogs = UnactedLogs.objects.filter(
        time_stamp__gte=start_date, 
        time_stamp__lt=end_date,
        user_id_id=user_id
    )

    delayed_count = unactedlogs.filter(is_acted=True).count()
    unacted_count = unactedlogs.filter(is_acted=False).count()

    data = {
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'delayed_count': delayed_count,
        'unacted_count': unacted_count
    }

    return JsonResponse(data)

def admin_officer_archived(request, time_span):

    # today: Today, Yesterday, 2 Days Before, 3 Days Before 4 Days Before, 5 Days Before, 6 Days Before
    # month: current month...... last 7th month
    # year: current year...... last 7th year
    today = timezone.now().date()

    if time_span == 'today':

        labels = ['6 Days Before', '5 Days Before', '4 Days Before', '3 Days Before', '2 Days Before', 'Yesterday', 'Today']
        values = []

        for i in range(6, -1, -1):

            target_date = today - timedelta(days=i)
            
            target_date_start = make_aware(datetime.combine(target_date, datetime.min.time()))
            target_date_end = make_aware(datetime.combine(target_date, datetime.max.time()))

            count = Document.objects.filter(
                status='Archived',
                recent_update__range=(target_date_start, target_date_end)
            ).count()

            values.append(count)
        
    elif time_span == 'month':

        labels = []
        values = []

        for i in range(7):
            month_offset = today - relativedelta(months=i)
            month_name = month_offset.strftime('%B')
            labels.append(month_name)

            start_of_month = month_offset.replace(day=1)
            end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)

            start_of_month = timezone.make_aware(datetime.combine(start_of_month, datetime.min.time()))
            end_of_month = timezone.make_aware(datetime.combine(end_of_month, datetime.max.time()))
            
            count = Document.objects.filter(
                status='Archived',
                recent_update__range=(start_of_month, end_of_month)
            ).count()
            
            values.append(count)

        labels.reverse()
        values.reverse()
    
    else:
        current_year = today.year
        labels = []
        values = []

        for i in range(7):
            year = current_year - i
            labels.append(year)

            start_of_year = make_aware(datetime(year, 1, 1, 0, 0, 0))  # January 1st
            end_of_year = make_aware(datetime(year, 12, 31, 23, 59, 59))  # December 31st

            count = Document.objects.filter(
                status='Archived',
                recent_update__range=(start_of_year, end_of_year)
            ).count()

            values.append(count)

        labels.reverse()
        values.reverse()

    print(values)

    data = {
        'labels': labels,
        'values': values
    }

    return JsonResponse(data)

def sro_total_records(request, time_span, target_prio_level):

    user_profile = request.session.get('user_profile', None)

    if user_profile:
        office = user_profile.get('office')
    else:
        return redirect(user_login)

    start_date, end_date = get_time_span(time_span)

    if target_prio_level == 'all':
        records = Document.objects.filter(
            status__in = ['For Routing', 'For SRO Receiving', 'For Resolving'],
            next_route = office,
            recent_update__gte=start_date, 
            recent_update__lt=end_date
        )
    else:
        records = Document.objects.filter(
            status__in = ['For Routing', 'For SRO Receiving', 'For Resolving'],
            next_route = office,
            document_type__priority_level__priority_level = target_prio_level,
            recent_update__gte=start_date, 
            recent_update__lt=end_date
        )
    
    data = {
        'act_forwarding': records.filter(status='For SRO Receiving').count(),
        'routing': records.filter(status='For Routing').count(),
        'resolving': records.filter(status='For Resolving').count()
    }

    return JsonResponse(data)

def sro_performance(request, time_span, target_performance):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_profile = request.session.get('user_profile', None)

    if user_profile:
        office = user_profile.get('office')
    else:
        return redirect(user_login)

    start_date, end_date = get_time_span(time_span)

    if target_performance == 'my-performance':

        resolved_count = ActivityLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            activity='Document Resolved',
            user_id_id = user_id
        ).count()

        pending_count = Document.objects.filter(
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            status__in = ["For Resolving", "For SRO Receiving"],
            next_route = office
        ).count()

    else:
        
        resolved_count = ActivityLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            activity='Document Resolved',
            user_id_id = user_id
        ).count()

        pending_count = Document.objects.filter(
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            status__in = ["For Resolving", "For SRO Receiving", "For ACT Receiving"],
            next_route = office
        ).count()

    unactedlogs = UnactedLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            user_id_id=user_id
        )

    delayed_count = unactedlogs.filter(is_acted=True).count()
    unacted_count = unactedlogs.filter(is_acted=False).count()

    data = {
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'delayed_count': delayed_count,
        'unacted_count': unacted_count
    }

    return JsonResponse(data)

def sro_employee_performance(request, time_span, target_employee_performance):


    data = {
        'success': 'success'
    }

    return JsonResponse(data)

def action_officer_total_records(request, time_span, target_prio_level):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    start_date, end_date = get_time_span(time_span)

    if target_prio_level == 'all':

        completed_count = ActivityLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            activity='Document Endorsed by Action Officer',
            user_id_id = user_id
        ).count()

        unacted_count = UnactedLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            user_id_id=user_id
        ).count()

        for_receive_count = Document.objects.filter(
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            status = 'For ACT Receiving',
            act_receiver = user_id
        ).count()

    else:

        completed_count = ActivityLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            activity='Document Endorsed by Action Officer',
            user_id_id = user_id,
            document_id__document_type__priority_level__priority_level = target_prio_level
        ).count()

        unacted_count = UnactedLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            user_id_id=user_id,
            document_id__document_type__priority_level__priority_level = target_prio_level
        ).count()

        for_receive_count = Document.objects.filter(
            recent_update__gte=start_date, 
            recent_update__lt=end_date,
            status = 'For ACT Receiving',
            act_receiver = user_id,
            document_type__priority_level__priority_level = target_prio_level
        ).count()


    data = {
        'completed_count': completed_count,
        'unacted_count': unacted_count,
        'for_receive_count': for_receive_count
    }

    return JsonResponse(data)

def action_officer_performance(request, time_span):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    start_date, end_date = get_time_span(time_span)

    endorsed_count = ActivityLogs.objects.filter(
        activity='Document Endorsed by Action Officer',
        user_id_id=user_id,
        time_stamp__gte=start_date, 
        time_stamp__lt=end_date,
    ).count()

    pending_count = Document.objects.filter(
        status='For ACT Receiving',
        act_receiver=user_id,
        recent_update__gte=start_date, 
        recent_update__lt=end_date,
    ).count()

    unacted_count = UnactedLogs.objects.filter(
            time_stamp__gte=start_date, 
            time_stamp__lt=end_date,
            user_id_id=user_id
    ).count()
    
    data = {
        'values': [endorsed_count, pending_count, unacted_count]
    }

    return JsonResponse(data)


# ------------------ NOTIFICATIONS -----------------------

def fetch_new_notifications(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)
    
    two_hours_ago = timezone.now() - timedelta(hours=2)

    role = user_id.split('-')[0]

    document_due_today = DocumentDueLogs.objects.filter(
        due_type='today',
        user_id_id=user_id,
        time_stamp__gte=two_hours_ago
    ).annotate(notification_type=F('due_type'))

    document_due_tomorrow = DocumentDueLogs.objects.filter(
        due_type='tomorrow',
        user_id_id=user_id,
        time_stamp__gte=two_hours_ago
    ).annotate(notification_type=F('due_type'))

    document_unacted = UnactedLogs.objects.filter(
        is_acted=False,
        user_id_id=user_id,
        time_stamp__gte=two_hours_ago
    ).annotate(notification_type=Value('Unacted'))

    if role == 'DIR':

        document_created = ActivityLogs.objects.filter(
            activity='Document Created',
            time_stamp__gte=two_hours_ago
        ).annotate(notification_type=F('activity'))

        document_reuploaded = ActivityLogs.objects.filter(
            activity='Document Reupload',
            time_stamp__gte=two_hours_ago
        ).annotate(notification_type=F('activity'))

        document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            time_stamp__gte=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_notifications = sorted(
            chain(document_created, document_reuploaded, document_resolved, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'ADO':

        document_approved = ActivityLogs.objects.filter(
            activity='Document Approved',
            time_stamp__gte=two_hours_ago
        ).annotate(notification_type=F('activity'))

        all_notifications = sorted(
            chain(document_approved, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )
    
    elif role == 'SRO':

        document_routed = ActivityLogs.objects.filter(
            activity='Document Routed',
            time_stamp__gte=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        document_endorsed = ActivityLogs.objects.filter(
            activity='Document Endorsed by Action Officer',
            time_stamp__gte=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            time_stamp__gte=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_notifications = sorted(
            chain(document_routed, document_endorsed, document_resolved, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'ACT':

        document_forwarded = ActivityLogs.objects.filter(
            activity='Document Forwarded to Action Officer',
            time_stamp__gte=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_notifications = sorted(
            chain(document_forwarded, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )
    
    if not all_notifications:
        return JsonResponse({'html': ''})

    context = {
        'notifications': all_notifications
    }

    html = render_to_string('partials/notification-instances.html', context)
    return JsonResponse({'html': html})

def fetch_earlier_notifications(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)
    
    role = user_id.split('-')[0]

    now = timezone.now()
    two_hours_ago = now - timedelta(hours=2)
    thirty_days_ago = now - timedelta(days=30)

    document_due_today = DocumentDueLogs.objects.filter(
        due_type='today',
        user_id_id=user_id,
        time_stamp__gte=thirty_days_ago,
        time_stamp__lt=two_hours_ago
    ).annotate(notification_type=F('due_type'))

    document_due_tomorrow = DocumentDueLogs.objects.filter(
        due_type='tomorrow',
        user_id_id=user_id,
        time_stamp__gte=thirty_days_ago,
        time_stamp__lt=two_hours_ago
    ).annotate(notification_type=F('due_type'))

    document_unacted = UnactedLogs.objects.filter(
        is_acted=False,
        user_id_id=user_id,
        time_stamp__gte=thirty_days_ago,
        time_stamp__lt=two_hours_ago
    ).annotate(notification_type=Value('Unacted'))

    if role == 'DIR':
    
        document_created = ActivityLogs.objects.filter(
            activity='Document Created',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago
        ).annotate(notification_type=F('activity'))

        document_reuploaded = ActivityLogs.objects.filter(
            activity='Document Reupload',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago
        ).annotate(notification_type=F('activity'))

        document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_earlier_notifications = sorted(
            chain(document_created, document_reuploaded, document_resolved, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    if role == 'ADO':

        document_approved = ActivityLogs.objects.filter(
            activity='Document Approved',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago
        ).annotate(notification_type=F('activity'))

        all_earlier_notifications = sorted(
            chain(document_approved, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )
    
    elif role == 'SRO':

        document_routed = ActivityLogs.objects.filter(
            activity='Document Routed',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        document_endorsed = ActivityLogs.objects.filter(
            activity='Document Endorsed by Action Officer',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_earlier_notifications = sorted(
            chain(document_routed, document_resolved, document_endorsed, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'ACT':

        document_forwarded = ActivityLogs.objects.filter(
            activity='Document Forwarded to Action Officer',
            time_stamp__gte=thirty_days_ago,
            time_stamp__lt=two_hours_ago,
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        all_earlier_notifications = sorted(
            chain(document_forwarded, document_due_today, document_due_tomorrow, document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )
    
    if not all_earlier_notifications:
        return JsonResponse({'html': ''})

    # Render the notifications into HTML
    context = {
        'notifications': all_earlier_notifications
    }

    html = render_to_string('partials/notification-instances.html', context)
    return JsonResponse({'html': html})

def fetch_unread_notifications(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)

    role = user_id.split('-')[0]

    unread_document_due_today = DocumentDueLogs.objects.filter(
        due_type='today',
        is_read='unread',
        user_id_id=user_id
    ).annotate(notification_type=F('due_type'))

    unread_document_due_tomorrow = DocumentDueLogs.objects.filter(
        due_type='tomorrow',
        is_read='unread',
        user_id_id=user_id
    ).annotate(notification_type=F('due_type'))

    unread_document_unacted = UnactedLogs.objects.filter(
        is_acted=False,
        is_read='unread',
        user_id_id=user_id
    ).annotate(notification_type=Value('Unacted'))

    if role == 'DIR':

        unread_document_created = ActivityLogs.objects.filter(
            activity='Document Created',
            is_read='unread'
        ).annotate(notification_type=F('activity'))

        unread_document_reuploaded = ActivityLogs.objects.filter(
            activity='Document Reupload',
            is_read='unread'
        ).annotate(notification_type=F('activity'))

        unread_document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            receiver_id_id = user_id,
            is_read='unread'
        ).annotate(notification_type=F('activity'))

        all_unread_notifications = sorted(
            chain(unread_document_created, unread_document_reuploaded, unread_document_resolved, unread_document_due_today, unread_document_due_tomorrow, unread_document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'ADO':
        
        unread_document_approved = ActivityLogs.objects.filter(
            activity='Document Approved',
            is_read='unread'
        ).annotate(notification_type=F('activity'))

        all_unread_notifications = sorted(
            chain(unread_document_approved, unread_document_due_today, unread_document_due_tomorrow, unread_document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'SRO':

        document_routed = ActivityLogs.objects.filter(
            activity='Document Routed',
            is_read='unread',
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        document_endorsed = ActivityLogs.objects.filter(
            activity='Document Endorsed by Action Officer',
            is_read='unread',
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))

        unread_document_resolved = ActivityLogs.objects.filter(
            activity='Document Resolved',
            receiver_id_id = user_id,
            is_read='unread'
        ).annotate(notification_type=F('activity'))

        all_unread_notifications = sorted(
            chain(document_routed, document_endorsed, unread_document_resolved, unread_document_due_today, unread_document_due_tomorrow, unread_document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )

    elif role == 'ACT':

        document_forwarded = ActivityLogs.objects.filter(
            activity='Document Forwarded to Action Officer',
            is_read='unread',
            receiver_id_id = user_id
        ).annotate(notification_type=F('activity'))



        all_unread_notifications = sorted(
            chain(document_forwarded, unread_document_due_today, unread_document_due_tomorrow, unread_document_unacted),
            key=lambda x: x.time_stamp,
            reverse=True
        )
    
    if not all_unread_notifications:
        return JsonResponse({'html': ''})

    context = {
        'notifications': all_unread_notifications
    }

    html = render_to_string('partials/notification-instances.html', context)

    return JsonResponse({'html': html})

def click_notification(request, notification_type, no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(user_login)

    if notification_type in ['Document Created', 'Document Reupload', 'Document Approved', 'Document Routed', 'Document Endorsed by Action Officer', 'Document Resolved']:
        document = ActivityLogs.objects.get(no=no)
    
    elif notification_type in ['today', 'tomorrow']:
        document = DocumentDueLogs.objects.get(no=no)

    elif notification_type == 'Unacted':
        document = UnactedLogs.objects.get(no=no)
        role = user_id.split('-')[0]
        if role == 'ACT':
            return redirect('action_officer_unacted_records')

    document.is_read = 'read'
    document.save()
    return redirect('scanning_qr_code', document.document_id.document_no)   


def fetch_document_routes(request, document_no):

    document = Document.objects.get(document_no=document_no)

    routes = DocumentRoute.objects.filter(document_type=document.document_type).values_list('route__office_name', flat=True)

    routes_list = list(routes)

    data = {
        'priority_level': document.document_type.priority_level.priority_level,
        'routes': routes_list
    }

    return JsonResponse(data)


def select_document(request, action, document_no):

    selected_documents = request.session.get('selected_documents', [])

    if action == 'checked':
        selected_documents.append(document_no)
    else:
        selected_documents.remove(document_no)

    request.session['selected_documents'] = selected_documents

    data = {
        'success': 'success'
    }

    return JsonResponse(data)

def select_all_documents(request, action):

    if request.method == 'POST':
        body = json.loads(request.body)
        documents_no = list(map(int, body.get('documents_no', [])))
        
        if action == 'select-all':
            request.session['selected_documents'] = documents_no

        elif action == 'deselect-all':
            selected_documents = request.session.get('selected_documents')
            if selected_documents:
                del request.session['selected_documents']
            
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)






