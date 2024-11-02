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


#---------------
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import IntegrityError
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
"""
# SYSTEM ADMIN LOGIN
def system_admin_login(request):

    user_id = request.session.get('user_id')
    if  user_id:
        role = user_id.split('-')[0]
        if role == 'ADO':
            return redirect(admin_officer_dashboard)
        elif role == 'SRO':
            return redirect(sro_dashboard)
        elif role == 'ACT':
            return redirect(action_officer_dashboard)
        elif role == 'DIR':
            return redirect(director_dashboard)
        elif role == 'SYS':
            return redirect(system_admin_dashboard)
    else:
        pass

    # Default credentials
    default_user_id = 'SYS-0001'
    default_password = 'SysAdmin@2024'

    if request.method == 'POST':
        form = SystemAdminLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            # Check if the provided credentials match the default credentials
            if user_id == default_user_id and password == default_password:
                # Ensure the default user exists and is active
                user_instance, created = User.objects.get_or_create(
                    user_id=default_user_id,
                    defaults={'password': default_password, 'role': 'System Admin', 'status': 'active'}
                )

                if created:
                    print(f"Default user {default_user_id} was created and set to active.")
                else:
                    # Update status if user already exists but not active
                    if user_instance.status != 'active':
                        user_instance.status = 'active'
                        user_instance.save()
                        print(f"Default user {default_user_id} status was updated to active.")

                # Store the credentials in session to keep the user logged in
                request.session['user_id'] = default_user_id
                request.session['user_name'] = user_instance.firstname.title() + " " + user_instance.lastname.title()

                # Redirect to the system admin dashboard
                return redirect(f"{reverse('system_admin_dashboard')}?status=active")
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = SystemAdminLoginForm()

    return render(request, "system_admin/system-admin-login.html", {'form': form})

# DIRECTOR LOGIN
def director_login(request):

    user_id = request.session.get('user_id')
    if  user_id:
        role = user_id.split('-')[0]
        if role == 'ADO':
            return redirect(admin_officer_dashboard)
        elif role == 'SRO':
            return redirect(sro_dashboard)
        elif role == 'ACT':
            return redirect(action_officer_dashboard)
        elif role == 'DIR':
            return redirect(director_dashboard)
        elif role == 'SYS':
            return redirect(system_admin_dashboard)
    else:
        pass

    # Default credentials
    default_user_id = 'DIR-0001'
    default_password = 'Director@2024'

    if request.method == 'POST':
        form = DirectorLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            # Check if the provided credentials match the default credentials
            if user_id == default_user_id and password == default_password:
                # Ensure the default user exists and is active
                user_instance, created = User.objects.get_or_create(
                    user_id=default_user_id,
                    defaults={'password': default_password, 'role': 'Director', 'status': 'active'}
                )   

                if created:
                    print(f"Default user {default_user_id} was created and set to active.")
                else:
                    # Update status if user already exists but is not active
                    if user_instance.status != 'active':
                        user_instance.status = 'active'
                        user_instance.save()
                        print(f"Default user {default_user_id} status was updated to active.")

                # Store the credentials in session to keep the user logged in
                request.session['user_id'] = default_user_id
                request.session['user_name'] = user_instance.firstname.title() + " " + user_instance.lastname.title()

                # Redirect to the director's dashboard
                return redirect(f"{reverse('director_dashboard')}?status=active")
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = DirectorLoginForm()

    return render(request, "director-login.html", {'form': form})

# USER LOGIN
def user_login(request):

    user_id = request.session.get('user_id')
    if  user_id:
        role = user_id.split('-')[0]
        if role == 'ADO':
            return redirect(admin_officer_dashboard)
        elif role == 'SRO':
            return redirect(sro_dashboard)
        elif role == 'ACT':
            return redirect(action_officer_dashboard)
        elif role == 'DIR':
            return redirect(director_dashboard)
        elif role == 'SYS':
            return redirect(system_admin_dashboard)
    else:
        pass

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

        user.last_login = timezone.now()
        user.save()

        request.session['user_id'] = user_id
        request.session['user_name'] = user.firstname.title() + " " + user.lastname.title()

        role = user_id.split('-')[0]

        # Redirect based on user role
        if role == 'ADO':  # Admin Officer
            return redirect(f"{reverse('admin_officer_dashboard')}?status=active")
        elif role == 'SRO':  # Sub-Receiving Officer
            return redirect(f"{reverse('sro_dashboard')}?status=active")
        elif role == 'ACT':  # Action Officer
            return redirect(f"{reverse('action_officer_dashboard')}?status=active")
        else:
            # In case the role is not recognized
            messages.error(request, "Invalid role. Please contact the administrator.")
            return redirect('user_login')

    return render(request, "user-login.html")
"""

# USER LOGIN
def user_login(request):

    # Check if a user is already logged in
    user_id = request.session.get('user_id')
    if user_id:
        role = user_id.split('-')[0]
        if role == 'ADO':
            return redirect(admin_officer_dashboard)
        elif role == 'SRO':
            return redirect(sro_dashboard)
        elif role == 'ACT':
            return redirect(action_officer_dashboard)
        elif role == 'DIR':
            return redirect(director_dashboard)
        elif role == 'SYS':
            return redirect(system_admin_dashboard)

    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']

        try:
            user = User.objects.get(user_id=user_id, password=password)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return redirect('user_login')

        user.last_login = timezone.now()
        user.save()
        request.session['user_id'] = user.user_id
        request.session['user_name'] = f"{user.firstname.title()} {user.lastname.title()}"

        # Redirect based on user role
        if user.role == 'ADO':
            return redirect(f"{reverse('admin_officer_dashboard')}?status=active")
        elif user.role == 'SRO':
            return redirect(f"{reverse('sro_dashboard')}?status=active")
        elif user.role == 'ACT':
            return redirect(f"{reverse('action_officer_dashboard')}?status=active")
        elif user.role == 'Director':
            return redirect(f"{reverse('director_dashboard')}?status=active")
        elif user.role == 'System Admin':
            return redirect(f"{reverse('system_admin_dashboard')}?status=active")
        else:
            messages.error(request, "Invalid role. Please contact the administrator.")
            return redirect('user_login')

    return render(request, "user-login.html")
# USER LOGOUT
def user_logout(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if user_id:
        del request.session['user_id']
        del request.session['user_name']
    
    if role == 'DIR':
        return redirect(user_login)
    elif role == 'SYS':
        return redirect(user_login)

    return redirect(user_login)

# -------------- DASHBOARD -------------------

# SYSTEM ADMIN DASHBOARD
def system_admin_dashboard(request):
    
    user_id = request.session.get('user_id')
    if  user_id:
        pass
    else:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    return render(request, 'system_admin/system-admin-dashboard.html', {'user_name': user_name})

# DIRECTOR DASHBOARD
def director_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    context = {
        'user_name': user_name
    }

    return render(request, 'director/director-dashboard.html', context)

# ADMIN OFFICER DASHBOARD
def admin_officer_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    return render(request, 'admin_officer/admin-officer-dashboard.html', {'user_name': user_name})

# SRO DASHBOARD
def sro_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'SRO':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    return render(request, 'sro/sro-dashboard.html', {'user_name': user_name})

# ACTION OFFICER DASHBOARD
def action_officer_dashboard(request):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'ACT':
        return redirect(user_login)
    
    user_name = request.session.get('user_name')

    return render(request, 'action_officer/action-officer-dashboard.html', {'user_name': user_name})

# -------------- USER MANAGEMENT -------------------

# SYSTEM ADMIN USER MANAGEMENT MODULE
def system_admin_user_management(request, office):

    user_id = request.session.get('user_id')
    if  not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    context = {
        'office': office,
        'user_name': user_name
    }

    return render(request, 'system_admin/system-admin-user-management.html', context)

# DIRECTOR USER MANAGEMENT MODULE
def director_user_management(request, office):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name,
        'office': office
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

    user_name = request.session.get('user_name')

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
    
    records = []

    document_type_records = DocumentType.objects.filter(is_active=True).order_by('-last_update')

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if sort_by in ['document_type', 'category', 'priority_level_id', 'email']:  # Only allow sorting by valid fields
        if order == 'asc':
            document_type_records = document_type_records.order_by(sort_by)
        else:
            document_type_records = document_type_records.order_by(f'-{sort_by}')

    routes = DocumentRoute.objects.all()

    for document_type_record in document_type_records:
        record = {}
        record['document_no'] = document_type_record.document_no
        record['document_type'] = document_type_record.document_type
        record['category'] = document_type_record.category
        record['priority_level'] = document_type_record.priority_level.priority_level

        temp_route = []
        for route in routes:
            if route.document_type_id == document_type_record.document_no:
                temp_route.append(route.route.office_name)
        record['routes'] = temp_route
        records.append(record)

    context = {
        'records': records,
        'user_name': user_name
    }

    return render(request, 'system_admin/system-admin-doc-management.html', context)

# SYSTEM ADMIN DOC MANAGEMENT
def director_doc_management(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)

    user_name = request.session.get('user_name')
    
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
    
    records = []

    document_type_records = DocumentType.objects.filter(is_active=True).order_by('-last_update')

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if sort_by in ['document_type', 'category', 'priority_level_id', 'email']:  # Only allow sorting by valid fields
        if order == 'asc':
            document_type_records = document_type_records.order_by(sort_by)
        else:
            document_type_records = document_type_records.order_by(f'-{sort_by}')

    routes = DocumentRoute.objects.all()

    for document_type_record in document_type_records:
        record = {}
        record['document_no'] = document_type_record.document_no
        record['document_type'] = document_type_record.document_type
        record['category'] = document_type_record.category
        record['priority_level'] = document_type_record.priority_level.priority_level

        temp_route = []
        for route in routes:
            if route.document_type_id == document_type_record.document_no:
                temp_route.append(route.route.office_name)
        record['routes'] = temp_route
        records.append(record)

    context = {
        'user_name': user_name,
        'records': records
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

    user_name = request.session.get('user_name')

    return render(request, 'system_admin/system-admin-new-record.html', {'user_name': user_name})

# ADMIN OFFICER NEW RECORD
def admin_officer_new_record(request):

    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    return render(request, 'admin_officer/admin-officer-new-record.html', {'user_name': user_name})

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

        if Document.objects.filter(tracking_no=tracking_no).exists():

            data = {
                'trackingNo': tracking_no,
                'recordExists': True
            }

            return JsonResponse(data)

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
        
        # Return a JSON response indicating success
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

    user_name = request.session.get('user_name')

    return render(request, 'system_admin/system-admin-all-records.html', {'user_name': user_name})

# ADMIN OFFICER ALL RECORDS
def admin_officer_all_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'ADO':
        return redirect(user_login)

    user_name = request.session.get('user_name')

    return render(request, 'admin_officer/admin-officer-all-records.html', {'user_name': user_name})

# DIRECTOR ALL RECORDS
def director_all_records(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
    }

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

    user_name = request.session.get('user_name')

    if int(scanned_document_no) < 0:
        return render(request, 'sro/sro-records.html', {'panel': panel, 'user_name': user_name})
    
    user = User.objects.get(user_id=user_id)
    office = user.office_id_id

    document = Document.objects.get(document_no=scanned_document_no)

    if not document:
        scanned_status = "not-found"
    elif document.status in ["For SRO Receiving", "For Resolving"] and document.next_route == office:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_name': user_name,
        'panel': panel,
        'scanned_status': scanned_status,
        'document': document
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

    user_name = request.session.get('user_name')

    if int(scanned_document_no) < 0:
        return render(request, 'action_officer/action-officer-records.html', {'user_name': user_name})

    user = User.objects.get(user_id=user_id)

    document = Document.objects.get(document_no=scanned_document_no)

    if not document:
        scanned_status = "not-found"
    elif document.status == 'For ACT Receiving' and document.next_route == user.office_id_id and document.act_receiver == user_id:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_name': user_name,
        'scanned_status': scanned_status,
        'document': document
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
        return redirect(user_login)

    user_name = request.session.get('user_name')

    if int(scanned_document_no) < 0:
        return render(request, 'admin_officer/admin-officer-needs-action.html', {'panel': panel, 'user_name': user_name})    

    document = Document.objects.get(document_no=scanned_document_no)

    if not document:
        scanned_status = "not-found"
    elif document.status in ["For Routing", "For Archiving"]:
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'
    
    context = {
        'user_name': user_name,
        'panel': panel,
        'scanned_status': scanned_status,
        'document': document
    }
    return render(request, 'admin_officer/admin-officer-needs-action.html', context) 

# DIRECTOR NEEDS ACTION
def director_needs_action(request, scanned_document_no):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    role = user_id.split('-')[0]
    if role != 'DIR':
        return redirect(user_login)
    
    user_name = request.session.get('user_name')

    if int(scanned_document_no) < 0:
        return render(request, 'director/director-needs-action.html', {'user_name': user_name})

    document = Document.objects.get(document_no=scanned_document_no)

    if not document:
        scanned_status = "not-found"
    elif document.status == 'For DIR Approval':
        scanned_status = 'authorized'
    else:
        scanned_status = 'unauthorized'

    context = {
        'user_name': user_name,
        'scanned_status': scanned_status,
        'document': document
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
        return redirect(user_login)

    user_name = request.session.get('user_name')

    if activity_type == 'doc-management':

        doc_management_logs = DocumentManagementLogs.objects.filter(user_id=user_id)

        records = []

        routes = DocumentRoute.objects.all()

        for log in doc_management_logs:
            record = {}
            record['time_stamp'] = log.time_stamp
            record['document_no'] = log.document_type.document_no
            record['document_type'] = log.document_type.document_type
            record['category'] = log.document_type.category
            record['priority_level'] = log.document_type.priority_level.priority_level

            temp_route = []
            for route in routes:
                if route.document_type_id == log.document_type.document_no:
                    temp_route.append(route.route.office_name)
            record['routes'] = temp_route
            record['activity'] = log.activity

            records.append(record)

        context = {
            'role': role,
            'user_name': user_name,
            'activity_type': activity_type,
            'records': records
        }

        return render(request, 'assets/sys-dir-activity-logs.html', context)

    elif activity_type == 'reports':

        records = ReportManagementLogs.objects.filter(user_id=user_id)
        context = {
            'role': role,
            'user_name': user_name,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)
    
    elif activity_type == 'user-management':

        records = UserManagementLogs.objects.filter(user=user_id)
        context = {
            'role': role,
            'user_name': user_name,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)
    
    elif activity_type == 'records':

        records = ActivityLogs.objects.filter(user_id_id=user_id)
        context = {
            'role': role,
            'user_name': user_name,
            'activity_type': activity_type,
            'records': records
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)

    elif activity_type == 'recent':

        # Current date and time details
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        fifteen_days_start = today_start - timedelta(days=15)

        # Fetch logs
        document_logs = ActivityLogs.objects.filter(user_id_id=user_id)
        user_management_logs = UserManagementLogs.objects.filter(user=user_id)
        doc_management_logs = DocumentManagementLogs.objects.filter(user_id=user_id)
        report_logs = ReportManagementLogs.objects.filter(user_id=user_id)

        # Initialize lists
        today_logs = []
        yesterday_logs = []
        this_week_logs = []
        last_fifteen_days_logs = []

        # Organize logs by time periods
        for log in document_logs:
            if log.time_stamp >= today_start:
                today_logs.append({'type': 'document', 'log': log})
            elif yesterday_start <= log.time_stamp < today_start:
                yesterday_logs.append({'type': 'document', 'log': log})
            elif week_start <= log.time_stamp < yesterday_start:
                this_week_logs.append({'type': 'document', 'log': log})
            elif fifteen_days_start <= log.time_stamp < week_start:
                last_fifteen_days_logs.append({'type': 'document', 'log': log})

        for log in user_management_logs:
            if log.time_stamp >= today_start:
                today_logs.append({'type': 'user_management', 'log': log})
            elif yesterday_start <= log.time_stamp < today_start:
                yesterday_logs.append({'type': 'user_management', 'log': log})
            elif week_start <= log.time_stamp < yesterday_start:
                this_week_logs.append({'type': 'user_management', 'log': log})
            elif fifteen_days_start <= log.time_stamp < week_start:
                last_fifteen_days_logs.append({'type': 'document', 'log': log})

        for log in doc_management_logs:
            if log.time_stamp >= today_start:
                today_logs.append({'type': 'doc_management', 'log': log})
            elif yesterday_start <= log.time_stamp < today_start:
                yesterday_logs.append({'type': 'doc_management', 'log': log})
            elif week_start <= log.time_stamp < yesterday_start:
                this_week_logs.append({'type': 'doc_management', 'log': log})
            elif fifteen_days_start <= log.time_stamp < week_start:
                last_fifteen_days_logs.append({'type': 'document', 'log': log})

        for log in report_logs:
            if log.time_stamp >= today_start:
                today_logs.append({'type': 'report', 'log': log})
            elif yesterday_start <= log.time_stamp < today_start:
                yesterday_logs.append({'type': 'report', 'log': log})
            elif week_start <= log.time_stamp < yesterday_start:
                this_week_logs.append({'type': 'report', 'log': log})
            elif fifteen_days_start <= log.time_stamp < week_start:
                last_fifteen_days_logs.append({'type': 'document', 'log': log})

        # Sort the logs from latest to oldest based on time_stamp
        today_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        yesterday_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        this_week_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)
        last_fifteen_days_logs.sort(key=lambda x: x['log'].time_stamp, reverse=True)

        # Pass organized logs to the template
        context = {
            'role': role,
            'user_name': user_name,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs,
        }
        return render(request, 'assets/sys-dir-activity-logs.html', context)
        #return render(request, 'director/director-activity-logs.html', context)

    context = {
        'role': role,
        'user_name': user_name,
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

    user_name = request.session.get('user_name')

    if activity_type == 'all-activity':
        records = ActivityLogs.objects.filter(user_id_id=user_id)
        context = {
            'user_name': user_name,
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
            'user_name': user_name,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs
        }

        return render(request, 'sro/sro-activity-logs.html', context)

    context = {
        'user_name': user_name,
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
        return redirect(user_login)

    user_name = request.session.get('user_name')

    if activity_type == 'all-activity':

        records = ActivityLogs.objects.filter(user_id_id=user_id)
        context = {
            'user_name': user_name,
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
            'user_name': user_name,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs
        }

        return render(request, 'admin_officer/admin-officer-activity-logs.html', context)


    context = {
        'user_name': user_name,
        'activity_type': activity_type
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

    user_name = request.session.get('user_name')

    if activity_type == 'all-activity':
        records = ActivityLogs.objects.filter(user_id_id=user_id)
        context = {
            'user_name': user_name,
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
            'user_name': user_name,
            'activity_type': activity_type,
            'today_logs': today_logs,
            'yesterday_logs': yesterday_logs,
            'this_week_logs': this_week_logs,
            'last_fifteen_days_logs': last_fifteen_days_logs
        }

        return render(request, 'action_officer/action-officer-activity-logs.html', context)
    
    context = {
        'user_name': user_name,
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
        return redirect(user_login)
    
    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
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

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
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

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
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

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
    }

    return render(request, 'action_officer/action-officer-unacted-records.html', context)

# -------------- ARCHIVE -------------------
# SYSTEM ADMIN ARCHIVE
def system_admin_archive(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    role = user_id.split('-')[0]
    if role != 'SYS':
        return redirect(user_login)

    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
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
    
    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
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
    
    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
    }

    return render(request, 'admin_officer/admin-officer-archive.html', context)

# ------------------ GENERATE REPORTS ------------------

# SYSTEM ADMIN GENERATE REPORTS MODULE
def system_admin_generate_reports(request, report_type):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')
    
    user_name = request.session.get('user_name')

    if report_type == 'all-reports':
        reports = Reports.objects.all()
    elif report_type == 'employee-performance':
        reports = Reports.objects.filter(report_type='Employee Performance')
    elif report_type == 'office-performance':
        reports = Reports.objects.filter(report_type='Office Performance')

    context = {
        'user_name': user_name,
        'report_type': report_type,
        'reports': reports
    }

    return render(request, 'system_admin/system-admin-generate-reports.html', context)

# DIRECTOR GENERATE REPORTS MODULE
def director_generate_reports(request, report_type):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('user_login')
    
    user_name = request.session.get('user_name')

    if report_type == 'all-reports':
        reports = Reports.objects.filter(is_active=True)
    elif report_type == 'employee-performance':
        reports = Reports.objects.filter(report_type='Employee Performance', is_active=True)
    elif report_type == 'office-performance':
        reports = Reports.objects.filter(report_type='Office Performance', is_active=True)

    context = {
        'user_name': user_name,
        'report_type': report_type,
        'reports': reports
    }

    return render(request, 'director/director-generate-reports.html', context)

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

        # Adjusting the priority level if necessary
        if priority_level_str == 'For Preferential Action':
            priority_level_str = 'for pref. action'

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
            elif status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__category')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving"], next_route=next_route).order_by('document_type__category')
        # For Due
        elif sort_by == 'deadline':
            if status == 'For ACT Forwarding':
                documents = Document.objects.filter(status="For SRO Receiving", next_route=next_route).order_by('document_type__priority_level__deadline')
            if status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__priority_level__deadline')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving"], next_route=next_route).order_by('document_type__priority_level__deadline')
        # For Priority Level
        else:
            if status == 'For ACT Forwarding':
                documents = Document.objects.filter(status="For SRO Receiving", next_route=next_route).order_by('document_type__priority_level__priority_level')
            elif status == 'For Resolving':
                documents = Document.objects.filter(status="For Resolving", next_route=next_route).order_by('document_type__priority_level__priority_level')
            else:
                documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving"], next_route=next_route).order_by('document_type__priority_level__priority_level')

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
            else:
                # If it's the last route
                status = 'For Archiving'

        else:
            if routes.count() == 1 and routes.first().route_id == 'DIR':
                status = 'For Archiving'
            else:
                status = 'For Routing'

        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)

        activity = 'Document Approved'

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
        initial_officer = User.objects.filter(office_id_id = office, role = 'ACT', receive_recent = 0).first()

        #if wala, it means lahat na ng ACTO ay nakareceive, so reset nya
        if initial_officer == None:
            officers = User.objects.filter(office_id_id = office, role = 'ACT')

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

        #if meron, then siya magrereceive
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
                    act_receiver = User.objects.get(status='active', role='Director').user_id
                else:
                    status = 'For SRO Receiving'
                    act_receiver = User.objects.get(status='active', role='SRO', office_id_id=next_route).user_id

            else:
                # If it's the last route
                print("Last route reached")
                status = 'For Archiving'
        else:
            print("1 route only")
            status = 'For Archiving'

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
    new_remarks = Remarks.objects.create(
        remarks=""
    )

    log = ActivityLogs.objects.create(
        time_stamp=timezone.now(),
        activity=activity,
        document_id=document,
        user_id_id=user_id,
        remarks = new_remarks,
        receiver = act_receiver
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

# ---------- FETCHING --------------

def fetch_document_details(request, document_no):
    try:
        document = Document.objects.get(document_no=document_no)

        d_type = document.document_type.category
        d_type = d_type[0].upper() + d_type[1:]
        d_type += " - " + document.document_type.document_type.title()

        data = {
            'tracking_no': document.tracking_no,
            'sender_name': document.sender_name.title(),
            'status': document.status,
            'document_type': d_type,  # Assuming foreign key
            'priority': document.document_type.priority_level.priority_level.title(),
            'subject': document.subject,
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

            log = {
                'date': local_time.strftime('%Y-%m-%d'),
                'time': local_time.strftime('%I:%M %p').lstrip('0'),
                'user_id': activity.user_id_id,
                'name': f"{firstname} {middlename} {lastname}".strip(),
                'office': office,
                'role': role,
                'remarks': remarks,
                'file_attachment': file_attachment,
                'activity': activity.activity
            }
            log_entries.append(log)
        data['activity_logs'] = log_entries

        return JsonResponse(data)
    except Document.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

# ---------- PARTIALS --------------

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

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    most_priority_doc_type = DocumentType.objects.filter(priority_level__priority_level='very urgent').order_by('-used_count').first()
    documents = Document.objects.exclude(status='archived').order_by('-recent_update')

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, "All Records")

    context = {
        'documents': documents,
        'most_priority_doc_type': most_priority_doc_type,
        'search_query': search_query,
        'user': user,
        'today': date.today() 
    }

    html = render_to_string('partials/display-records.html', context)
    return JsonResponse({'html': html})

def admin_officer_update_needs_action_display(request, panel):

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if panel == 'For-DIR-Approval':
        documents = Document.objects.filter(status='For DIR Approval').order_by('-recent_update')
        status = "For DIR Approval"
    elif panel == 'For-Routing':
        documents = Document.objects.filter(status='For Routing').order_by('-recent_update')
        status = "For Routing"
    elif panel == 'For-Archiving':
        documents = Document.objects.filter(status='For Archiving').order_by('-recent_update')
        status = "For Archiving"
    else:
        documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving"]).order_by('-recent_update')
        status = "ADO - All Documents"

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, status)

    context = {
        'documents': documents,
        'search_query': search_query,
        'user': 'ADO',
        'today': date.today() 
    }

    html = render_to_string('partials/display-records.html', context)
    return JsonResponse({'html': html})

def director_update_needs_action_display(request):
    
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    most_priority_doc_type = DocumentType.objects.filter(priority_level__priority_level='very urgent').order_by('-used_count').first()
    documents = Document.objects.filter(status='For DIR Approval').order_by('-recent_update')

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents(documents, sort_by, order, "For DIR Approval")

    context = {
        'documents': documents,
        'most_priority_doc_type': most_priority_doc_type,
        'search_query': search_query,
        'user': 'DIR',
        'today': date.today()
    }

    html = render_to_string('partials/display-records.html', context)
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

    if panel == 'For-ACT-Forwarding':
        documents = Document.objects.filter(status='For SRO Receiving', next_route=office).order_by('-recent_update')
        status = 'For ACT Forwarding'
    elif panel == 'For-Resolving':
        documents = Document.objects.filter(status='For Resolving', next_route=office).order_by('-recent_update')
        status = 'For Resolving'
    else:
        documents = Document.objects.filter(status__in=["For SRO Receiving", "For Resolving"], next_route=office).order_by('-recent_update')
        status = 'SRO All Documents'

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents_sro(documents, sort_by, order, status, office)

    context = {
        'documents': documents,
        'search_query': search_query,
        'user': 'SRO',
        'today': date.today()
    }

    html = render_to_string('partials/display-records.html', context)
    return JsonResponse({'html': html})

def action_officer_update_records_display(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect(user_login)

    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    documents = Document.objects.filter(status='For ACT Receiving', act_receiver=user_id).order_by('-recent_update')

    if search_query:
        documents = search_documents(documents, search_query)

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields
        documents = sort_documents_act(documents, sort_by, order, user_id)

    context = {
        'documents': documents,
        'search_query': search_query,
        'user': 'ACT',
        'today': date.today()
    }

    html = render_to_string('partials/display-records.html', context)
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

    documents = Document.objects.filter(status='archived')

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
    user_name = request.session.get('user_name')

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
        return redirect(system_admin_generate_reports)
    elif role == 'DIR':
        return redirect(director_generate_reports)

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
        return redirect(system_admin_generate_reports)
    elif role == 'DIR':
        return redirect(director_generate_reports)

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
    user_name = request.session.get('user_name')

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
                receiver=User.objects.get(status='active', role='Director').user_id,
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
                receiver = report.employee_id_id,
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
                receiver = report.employee_id.user_id,
                time_stamp__range=[converted_start_date, converted_end_date]
            ).count()
            action_officer_total_received_documents += ActivityLogs.objects.filter(
                activity='Document Reassigned Due to Inaction',
                receiver=report.employee_id.user_id,
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
            time_stamp__range=[report.start_date, report.end_date]
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
            receiver=sro.user_id,
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
            time_stamp__range=[report.start_date, report.end_date]
        )

        for docu in delayed_logs: 
                tracking_no_parts = docu.document_id.tracking_no.split('-', 1)
                docu.tracking_no_first = tracking_no_parts[0]  
                docu.tracking_no_second = tracking_no_parts[1]
                docu.delayed_days = (docu.date_acted - docu.time_stamp).days

        unacted_logs = UnactedLogs.objects.filter(
            user_id__role__in=['SRO', 'ACT'],
            is_acted=False,
            time_stamp__range=[report.start_date, report.end_date]
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

    # If there was an error
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Performance-Report.pdf"'

    return response

# ------------------ ANNOUNCEMENTS -----------------------
def system_admin_announcements(request):

    user_id = request.session.get('user_id')
    role = user_id.split('-')[0]

    if not user_id:
        return redirect('user_login')
    
    user_name = request.session.get('user_name')
    context = {
        'user_name': user_name
    }

    return render(request, 'system_admin/system-admin-announcements.html', context)

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
        'highlighted_remarks': highlighted_remarks  # Include HTML string with highlighted words
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
            priority_level_id=4,
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
    return JsonResponse({'data': 'sucess'})