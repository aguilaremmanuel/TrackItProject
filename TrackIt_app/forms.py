from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib.auth.hashers import make_password

def is_valid_password(password):
    # Check if password has at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

class UserSignupForm(forms.ModelForm):
    OFFICE_CHOICES = [
        ('', 'Select Office'),
        ('ACC', 'Accounting'),
        ('BMD', 'Budgeting'),
        ('CSR', 'Cashier'),
        ('PRL', 'Payroll'),
    ]

    office_id = forms.ChoiceField(
        choices=OFFICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'selectOffice',
        })
    )

    ROLE_CHOICES = [
        ('', 'Select Role'),
        ('ACT', 'Action Officer'),
        ('SRO', 'Sub-Receiving Officer'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'selectRole',
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'id': 'password2',
            'placeholder': 'Confirm Password',
        })
    )
   
    class Meta:
        model = User
        fields = ['firstname','middlename','lastname','employee_id' ,'email', 'contact_no','role','password', 'registered_date']

        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Juan'
            }),
            'middlename': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Santos'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Dela Cruz'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 123456-ADM'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. juandelacruz@email.com'
            }),
            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                #'pattern': '09[0-9]{2} [0-9]{3} [0-9]{4}',
                'placeholder': 'e.g. 09123456789'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Enter Password'
            }),
        }

    # Make the middlename field optional
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['middlename'].required = False
    
    def clean(self):

        cleaned_data = super().clean()

        # CONFIRM PASSWORD VALIDATION        
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        # EMAIL VALIDATION 
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            pass
        
        # PASSWORD VALIDATION 
        if password and not is_valid_password(password):
            self.add_error('password', "Password must be at least 8 characters with a special character and an uppercase letter.")
        
        return cleaned_data
    
    
    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)

        # Hash the password using Django's make_password function
        # user.password = make_password(self.cleaned_data['password'])

        office_id = self.cleaned_data['office_id']
        office_instance = Office.objects.get(office_id=office_id)
        user.office_id = office_instance


        if commit:
            user.save()
        return user

class SystemAdminLoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User ID', 'id': 'user_id'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'id': 'password'})
    )


class DirectorLoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User ID', 'id': 'user_id'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'id': 'password'})
    )

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'attachment','end_date'] #
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # 
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'middlename', 'lastname', 'email', 'contact_no', 'profile_picture']



