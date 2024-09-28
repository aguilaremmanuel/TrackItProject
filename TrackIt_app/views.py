from django.shortcuts import render, redirect
from .forms import *
from django.db.models import Max
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import qrcode
from io import BytesIO
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import datetime
import pytz
import json


# ----------- LOGIN AND SIGNUP -----------------

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

# SYSTEM ADMIN LOGIN
def system_admin_login(request):
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
                request.session['system_admin_user_id'] = default_user_id
                request.session['role'] = 'SYSTEM_ADMIN'

                # Redirect to the system admin dashboard
                return redirect('system_admin_dashboard')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = SystemAdminLoginForm()

    return render(request, "system_admin/system-admin-login.html", {'form': form})

# DIRECTOR LOGIN
def director_login(request):
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
                request.session['director_user_id'] = default_user_id
                request.session['role'] = 'DIRECTOR'

                # Redirect to the director's dashboard
                return redirect('dashboard_director')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = DirectorLoginForm()

    return render(request, "director-login.html", {'form': form})

# USER LOGIN
def user_login(request):

    role = request.session.get('role')

    if role == 'ADO':
        return redirect(dashboard_admin_officer)
    elif role == 'SRO':
        return redirect(dashboard_sro)
    elif role == 'ACT':
        return redirect(dashboard_action_officer)
    elif role == 'SYSTEM_ADMIN':
        return redirect(system_admin_dashboard)
    elif role == 'DIRECTOR':
        return redirect(dashboard_director)
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
        request.session['role'] = user.role

        # Redirect based on user role
        if user.role == 'ADO':  # Admin Officer
            request.session['ado_user_id'] = user.user_id
            return redirect('dashboard_admin_officer')
        elif user.role == 'SRO':  # Sub-Receiving Officer
            request.session['sro_user_id'] = user.user_id
            return redirect('dashboard_sro')
        elif user.role == 'ACT':  # Action Officer
            request.session['act_user_id'] = user.user_id
            return redirect('dashboard_action_officer')
        else:
            # In case the role is not recognized
            messages.error(request, "Invalid role. Please contact the administrator.")
            return redirect('user_login')

    return render(request, "user-login.html")

# USER LOGOUT
def user_logout(request):

    role = request.session.get('role')

    if role == 'ADO':
        del request.session['ado_user_id']
    elif role == 'SRO':
        del request.session['sro_user_id']
    elif role == 'ACT':
        del request.session['act_user_id']
    elif role == 'SYSTEM_ADMIN':
        del request.session['system_admin_user_id']
        return redirect(system_admin_login)
    elif role == 'DIRECTOR':
        del request.session['director_user_id']
        return redirect(director_login)
        
    del request.session['role']
    return redirect(user_login)

# -------------- DASHBOARD -------------------

# SYSTEM ADMIN DASHBOARD
def system_admin_dashboard(request):
    system_admin_user_id = request.session.get('system_admin_user_id')

    if  system_admin_user_id:
        pass
    else:

        return redirect('system_admin_login')
    return render(request, 'system_admin/system-admin-dashboard.html')

# DIRECTOR DASHBOARD
def dashboard_director(request):
    director_user_id = request.session.get('director_user_id')

    if  director_user_id:
        pass
    else:
        return redirect('director_login')

    return render(request, 'director/director-dashboard.html')

# ADMIN OFFICER DASHBOARD
def dashboard_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-dashboard.html')

# SRO DASHBOARD
def dashboard_sro(request):
    return render(request, 'sro/sro-dashboard.html')

# ACTION OFFICER DASHBOARD
def dashboard_action_officer(request):
    return render(request, 'action_officer/action-officer-dashboard.html')

# -------------- USER MANAGEMENT -------------------

# SYSTEM ADMIN USER MANAGEMENT MODULE
def system_admin_user_management(request, office):
    system_admin_user_id = request.session.get('system_admin_user_id')

    if  system_admin_user_id:
        pass
    else:
        return redirect('system_admin_login')

    return render(request, 'system_admin/system-admin-user-management.html', {'office': office})

# DIRECTOR USER MANAGEMENT MODULE
def director_user_management(request, office):
    director_user_id = request.session.get('director_user_id')

    if  director_user_id:
        pass
    else:
        return redirect('director_login')

    return render(request, 'director/director-user-management.html', {'office': office})

# -------------- DOC MANAGEMENT -------------------

# SYSTEM ADMIN DOC MANAGEMENT
def system_admin_doc_management(request):
    system_admin_user_id = request.session.get('system_admin_user_id')

    if  system_admin_user_id:
        pass
    else:
        return redirect('system_admin_login')

    if request.method == 'POST':
        
        document_type = request.POST.get('document_type')
        category = request.POST.get('category')
        priority_level_str = request.POST.get('priority_level')
        route_list = request.POST.getlist('route[]')
        
        priority_level = PriorityLevel.objects.get(priority_level=priority_level_str)

        new_document_type = DocumentType.objects.create(
            document_type=document_type,
            category=category,
            priority_level=priority_level
        )

        for route in route_list:
            office = Office.objects.get(office_name=route)  # Fetch the Office instance
            DocumentRoute.objects.create(
                document_type=new_document_type,
                route=office
            )
    
    records = []

    document_type_records = DocumentType.objects.all()

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

    return render(request, 'system_admin/system-admin-doc-management.html', {'records': records})

# SYSTEM ADMIN DOC MANAGEMENT
def director_doc_management(request):
    director_user_id = request.session.get('director_user_id')

    if  director_user_id:
        pass
    else:
        return redirect('director_login')

    if request.method == 'POST':
        
        document_type = request.POST.get('document_type')
        category = request.POST.get('category')
        priority_level_str = request.POST.get('priority_level')
        route_list = request.POST.getlist('route[]')
        
        priority_level = PriorityLevel.objects.get(priority_level=priority_level_str)

        new_document_type = DocumentType.objects.create(
            document_type=document_type,
            category=category,
            priority_level=priority_level
        )

        for route in route_list:
            office = Office.objects.get(office_name=route)  # Fetch the Office instance
            DocumentRoute.objects.create(
                document_type=new_document_type,
                route=office
            )
    
    records = []

    document_type_records = DocumentType.objects.all()

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

    return render(request, 'director/director-doc-management.html', {'records': records})

# -------------- NEW RECORD -------------------

# SYSTEM ADMIN OFFICER NEW RECORD
def new_record_system_admin(request):

    system_admin_user_id = request.session.get('system_admin_user_id')

    if  system_admin_user_id:
        pass
    else:
        return redirect('system_admin_login')

    showQRModal = False
    qr_code_url = None
    str_routes, str_routes_titles, str_tracking_no = '', '', ''
    document_no = 0

    # Credentials are correct, proceed to handle new record creation
    if request.method == 'POST':
        tracking_no = request.POST.get('tracking_no')
        sender_name = request.POST.get('sender_name')
        sender_dept = request.POST.get('sender_dept')
        doc_type = request.POST.get('doc_type')
        subject = request.POST.get('subject')
        remarks = request.POST.get('remarks')

        document = create_document(tracking_no, sender_name, sender_dept, doc_type, subject, remarks, system_admin_user_id)

        routes = DocumentRoute.objects.filter(document_type=document.document_type)
        
        str_routes, str_routes_titles = generate_route_strings(routes)
        showQRModal = True
        qr_code_url = request.build_absolute_uri(f'/generate-qrcode/{document.document_no}/')
        str_tracking_no = tracking_no
        document_no = document.document_no


    return render(request, 'system_admin/system-admin-new-record.html', {
        'showQRModal': showQRModal, 
        'qr_code_url': qr_code_url, 
        'str_routes': str_routes,
        'str_routes_titles': str_routes_titles,
        'str_tracking_no': str_tracking_no,
        'document_no': document_no})

# ADMIN OFFICER NEW RECORD
def new_record_admin_officer(request):

    ado_user_id = request.session.get('ado_user_id')
    
    if ado_user_id:
        pass
    else:
        return redirect('user_login')

    showQRModal = False
    qr_code_url = None
    str_routes = ''
    str_routes_titles = ''
    str_tracking_no = ''
    document_no = 0

    if request.method == 'POST':

        tracking_no = request.POST.get('tracking_no')
        sender_name = request.POST.get('sender_name')
        sender_dept = request.POST.get('sender_dept')
        doc_type = request.POST.get('doc_type')
        subject = request.POST.get('subject')
        remarks = request.POST.get('remarks')


        if Document.objects.filter(tracking_no=tracking_no).exists():
            return redirect('new_record_admin_officer')

        document = create_document(tracking_no, sender_name, sender_dept, doc_type, subject, remarks, ado_user_id)

        routes = DocumentRoute.objects.filter(document_type=document.document_type)
        
        str_routes, str_routes_titles = generate_route_strings(routes)
        showQRModal = True
        qr_code_url = request.build_absolute_uri(f'/generate-qrcode/{document.document_no}/')
        str_tracking_no = tracking_no
        document_no = document.document_no

    return render(request, 'admin_officer/admin-officer-new-record.html', {
        'showQRModal': showQRModal, 
        'qr_code_url': qr_code_url, 
        'str_routes': str_routes,
        'str_routes_titles': str_routes_titles,
        'str_tracking_no': str_tracking_no,
        'document_no': document_no})

# -------------- ALL RECORDS -------------------

# ADMIN OFFICER ALL RECORDS
def all_records_admin_officer(request):

    ado_user_id = request.session.get('ado_user_id')

    if ado_user_id:
        pass
    else:
        return redirect('user_login')

    return render(request, 'admin_officer/admin-officer-all-records.html')

# -------------- RECORDS -------------------

# SRO ALL RECORDS
def all_records_sro(request):
    return render(request, 'sro/sro-all-records.html')

# ACTION OFFICER ALL RECORDS
def all_records_action_officer(request):

    document_no = request.GET.get('document_no')

    return render(request, 'action_officer/action-officer-all-records.html')

# -------------- NEEDS ACTION -------------------

# ADMIN OFFICER NEEDS ACTION
def admin_officer_needs_action(request, panel):

    ado_user_id = request.session.get('ado_user_id')

    if ado_user_id:
        pass
    else:
        return redirect('user_login')
    


    return render(request, 'admin_officer/admin-officer-needs-action.html', {'panel': panel})


# SRO UNACTED DOCUMENTS
def unacted_documents_sro(request):
    return render(request, 'sro/sro-unacted-documents.html')

# SRO ACTIVITY LOGS
def activity_logs_sro(request):
    return render(request, 'sro/sro-activity-logs.html')

# ADMIN OFFICER OVERDUE
def overdue_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-overdue.html')

# ADMIN OFFICER ARCHIVE
def archive_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-archive.html')

# ADMIN OFFICER ACTIVITY LOGS
def activity_logs_admin_officer(request):
    return render(request, 'admin_officer/admin-officer-activity-logs.html')

# ACTION OFFICER UNACTED DOCUMENTS
def unacted_documents_action_officer(request):
    return render(request, 'action_officer/action-officer-unacted-documents.html')

# ACTION OFFICER ACTIVITY LOGS
def activity_logs_action_officer(request):
    return render(request, 'action_officer/action-officer-activity-logs.html')


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
            # Attempt to fetch the user based on the user_id
            user = User.objects.get(user_id=user_id)

            # Check if the retrieved user's email matches the provided email
            if user.email != email:
                messages.error(request, "Email does not match the User ID provided.")
                return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        except User.DoesNotExist:
            # If the user is not found, provide a relevant error message
            messages.error(request, "User ID does not match any account.")
            return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        # Check user status
        if user.status not in ['active']:
            messages.error(request, "Your account cannot be used for password reset.")
            return render(request, 'forgot-password.html', {'displayForgotPassword': '', 'displayEmailConfirmation': 'd-none', 'displayPasswordSuccess': 'd-none'})

        # Generate reset link
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        #print(f"Generated Token: {token}")

        reset_link = request.build_absolute_uri(
            reverse('new_password', kwargs={'uidb64': uidb64, 'token': token})
        )

        # Send email
        try:
            subject = 'Reset your password'
            message = (
                f'Hello {user.firstname},\n\n'
                f'Click the link to reset your password: {reset_link}\n\n'
                'If you did not request a password reset, please ignore this email.\n\n'
                'Regards,\nTrackIt Team'
            )
            send_mail(
                subject,
                message,
                'trackit.dts@gmail.com',
                [user.email],
                fail_silently=False,
            )
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
        new_document_type.save()

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
    routes = DocumentRoute.objects.filter(document_type_id = document_no)
    routes.delete()
    document_type = DocumentType.objects.get(document_no=document_no)
    document_type.delete()

    return redirect('system_admin_doc_management')

# LOADING OF DOC TYPES
def load_document_types(request):
    category = request.GET.get('category')

    if category in ['SCPF', 'Regular']:
        document_types = DocumentType.objects.filter(category=category).values('document_no', 'document_type')
        return JsonResponse(list(document_types), safe=False)
    else:
        return JsonResponse({'error': 'Invalid category'}, status=400)

#USER UPDATE STATUS AND EMAILING FUNCTION
def update_user_status(request, user_id, action, office, user_type):
    user = User.objects.get(pk=user_id)

    # Perform action
    if action == 'verify':
        user.status = 'active'
        subject = 'Your Account Has Been Verified'
        message = f"Hello {user.firstname},\n\nYour account has been verified and is now active.\n\nYour User ID: {user.user_id}\nYour Password: {user.password}\n\nPlease keep this information secure.\n\nRegards,\nTrackIt Team"
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

    user.save()

    if action != 'archive':
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    # Redirect based on the form source

    if user_type == 'director':
        return redirect('director_user_management', office=office)
    else:
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
def create_document(tracking_no, sender_name, sender_dept, doc_type, subject, remarks, user_id):

    document_type_instance = DocumentType.objects.get(document_no=doc_type)

    document = Document.objects.create(
        tracking_no=tracking_no,
        sender_name=sender_name,
        sender_department=sender_dept,
        document_type=document_type_instance,
        subject=subject,
        remarks=remarks,
        status='For DIR Approval',
        recent_update = timezone.now()
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
        remarks = new_remarks
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

# FUNCTION FOR ALL ACTIONS (APPROVE, ROUTE, ARCHIVED...)
def document_update_status(request, action, document_no):
    
    role = request.session.get('role')

    if role == 'ADO':
        user_id = request.session.get('ado_user_id')
    elif role == 'SRO':
        user_id = request.session.get('sro_user_id')
    elif role == 'ACT':
        user_id = request.session.get('act_user_id')
    elif role == 'SYSTEM_ADMIN':
        user_id = request.session.get('system_admin_user_id')
    elif role == 'DIRECTOR':
        user_id = request.session.get('director_user_id')
    else:
        return redirect('user_login')

    document = Document.objects.get(document_no=document_no)

    if action == 'approve':
        status = 'For Routing'
        activity = 'Document Approved'

    elif action == 'route':
        status = 'For SRO Receiving'
        activity = 'Document Routed'

    elif action == 'forward-to-act':
        status = 'For ACT Receiving'
        activity = 'Document Received-SRO and Forwarded-ACT'

    elif action == 'endorse-resolve':
        status = 'For Resolving'
        activity = 'Document Endorsed-ACT'

    elif action == 'resolve':
        status = 'For Archiving'
        activity = 'Document Resolved'

    elif action == 'archive':
        status = 'Archived'
        activity = 'Document Archived'

    document = Document.objects.get(document_no=document_no)
    document.status = status
    document.recent_update = timezone.now()
    document.save()

    new_remarks = Remarks.objects.create(
        remarks=""
    )

    log = ActivityLogs.objects.create(
        time_stamp=timezone.now(),
        activity=activity,
        document_id=document,
        user_id_id=user_id,
        remarks = new_remarks
    )

    data = {'remarks_no': log.remarks_id}
    return JsonResponse(data)

    #approve = For Routing
    #route = For SRO Receiving
    #forward-to-act = For ACT Receiving
    #endorse-for-resolve = For Resolving
    #resolve = For Archiving
    #archive = Archived

def add_remarks(request, document_no, remarks_no):

    if request.method == 'POST':
        data = json.loads(request.body)
        remarks = data.get('remarksInput')
        print("remarks is: ", remarks)
        editRemarks = Remarks.objects.get(no=remarks_no)
        editRemarks.remarks = remarks
        editRemarks.save()
        
        document = Document.objects.get(document_no=document_no)
        document.remarks = remarks
        document.save()

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

        data = {
            'tracking_no': document.tracking_no,
            'sender_name': document.sender_name.title(),
            'status': document.status,
            'document_type': document.document_type.category,  # Assuming foreign key
            'priority': document.document_type.priority_level.priority_level.title(),
            'due_in': document.document_type.priority_level.deadline,  # Calculate if needed
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

            log = {
                'date': local_time.strftime('%Y-%m-%d'),
                'time': local_time.strftime('%I:%M %p').lstrip('0'),
                'user_id': activity.user_id_id,
                'name': f"{firstname} {middlename} {lastname}".strip(),
                'office': activity.user_id.office_id.office_name,
                'role': role,
                'remarks': remarks,
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

def update_all_records_display(request):

    search_query = request.GET.get('search', '').strip()

    documents = Document.objects.exclude(status='archived')

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if search_query:

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


    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields

        if sort_by == 'status':
            if order == 'asc':
                documents = documents.order_by(sort_by)
            else:
                documents = documents.order_by(f'-{sort_by}')
        else:

            if sort_by == 'document_type':
                documents = Document.objects.order_by('document_type__category')
            elif sort_by == 'deadline':
                documents = Document.objects.order_by('document_type__priority_level__deadline')
            else:
                documents = Document.objects.order_by('document_type__priority_level__priority_level')

    context = {
        'documents': documents,
        'search_query': search_query
    }

    html = render_to_string('partials/admin-officer-all-records.html', context)
    return JsonResponse({'html': html})

def admin_officer_update_needs_action_display(request, panel):

    search_query = request.GET.get('search', '').strip()

    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if panel == 'For-DIR-Approval':
        documents = Document.objects.filter(status='For DIR Approval')
    elif panel == 'For-Routing':
        documents = Document.objects.filter(status='For Routing')
    elif panel == 'For-Archiving':
        documents = Document.objects.filter(status='For Archiving')
    else:
        documents = Document.objects.filter(status__in=["For DIR Approval", "For Routing", "For Archiving"])

    if search_query:

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

    if sort_by in ['status', 'document_type', 'deadline', 'priority_level']:  # Only allow sorting by valid fields

        if sort_by == 'status':
            if order == 'asc':
                documents = documents.order_by(sort_by)
            else:
                documents = documents.order_by(f'-{sort_by}')
        else:

            if sort_by == 'document_type':
                documents = Document.objects.order_by('document_type__category')
            elif sort_by == 'deadline':
                documents = Document.objects.order_by('document_type__priority_level__deadline')
            else:
                documents = Document.objects.order_by('document_type__priority_level__priority_level')

    context = {
        'documents': documents,
        'search_query': search_query
    }

    html = render_to_string('partials/admin-officer-needs-action.html', context)
    return JsonResponse({'html': html})
