from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator, RegexValidator

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

# Validator to ensure only letters (letters and spaces only)
letter_only_validator = RegexValidator(
    regex=r'^[a-zA-Z ]+$',
    message='This field can only contain letters and spaces.'
)

# Validator to ensure only numbers (no letters, no special characters)
number_only_validator = RegexValidator(
    regex=r'^\d+$',  # Only digits allowed
    message='This field can only contain numbers.'
)

employee_id_validator = RegexValidator(
    regex=r'^\d{6}-[A-Za-z]{3}$',  # 6 digits, followed by a hyphen and 3 letters (e.g., 123456-ADM)
    message='Employee ID must be in the format 123456-ADM.'
)

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
            'id': 'selectOffice'
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
            'placeholder': 'Confirm Password'
        })
    )

    # Apply the validator and max length to firstname, middlename, and lastname fields
    firstname = forms.CharField(
        max_length=45,
        validators=[letter_only_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control letter-only',  # Add the letter-only class here
            'placeholder': 'e.g. Juan',
            'title': 'Only letters and spaces are allowed.'
        })
    )

    middlename = forms.CharField(
        max_length=45,
        required=False,
        validators=[letter_only_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control letter-only',  # Add the letter-only class here
            'placeholder': 'e.g. Santos',
            'title': 'Only letters and spaces are allowed.'
        })
    )

    lastname = forms.CharField(
        max_length=45,
        validators=[letter_only_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control letter-only',  # Add the letter-only class here
            'placeholder': 'e.g. Dela Cruz',
            'title': 'Only letters and spaces are allowed.'
        })
    )

    contact_no = forms.CharField(
        max_length=11,
        validators=[number_only_validator],  # Use the number-only validator
        widget=forms.TextInput(attrs={
            'class': 'form-control numbers-only',  # Add 'numbers-only' class here
            'placeholder': 'e.g. 09123456789',
            'title': 'Only numbers are allowed.'
        })
    )

    employee_id = forms.CharField(
        max_length=10, 
        validators=[employee_id_validator],  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'employeeID', 
            'placeholder': 'e.g. 123456-ADM',
            'title': '6 digits followed by a hyphen and 3 uppercase letters.'
        })
    )

    class Meta:
        model = User
        fields = ['firstname', 'middlename', 'lastname', 'employee_id', 'email', 'contact_no', 'role', 'password', 'registered_date']
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
                'placeholder': 'e.g. 09123456789'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Enter Password'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Confirm password validation
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        # Ensure 'Select Office' or 'Select Role' are not submitted
        if cleaned_data.get('office_id') == '':
            self.add_error('office_id', "Please select a valid office.")
        if cleaned_data.get('role') == '':
            self.add_error('role', "Please select a valid role.")

        # Email validation
        email = cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', "Enter a valid email address.")

        # Password validation
        if password and not is_valid_password(password):
            self.add_error('password', "Password must be at least 8 characters long, contain an uppercase letter, and a special character.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.password = make_password(self.cleaned_data['password'])  # Hash the password

        # Assign office instance
        office_id = self.cleaned_data['office_id']
        try:
            office_instance = Office.objects.get(office_id=office_id)
            user.office_id = office_instance
        except Office.DoesNotExist:
            raise ValidationError("Selected office does not exist.")

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

