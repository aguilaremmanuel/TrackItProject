from django import forms
from .models import *
from django.core.exceptions import ValidationError

class UserSignupForm(forms.ModelForm):

    DEPARTMENT_CHOICES = [
        ('', 'Select Department'),
        ('ADM', 'Administrative'),
        ('ACC', 'Accounting'),
        ('BMD', 'Budgeting'),
        ('CSR', 'Cashier'),
        ('PRL', 'Payroll'),
    ]

    office_id = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'selectDept',
        })
    )

    ROLE_CHOICES = [
        ('', 'Select Officer Role'),
        ('ADO', 'Admin Officer'),
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
        fields = ['firstname','middlename','lastname','employee_id' ,'email', 'contact_no', 'role','password', 'registered_date']

        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'e.g. Juan'
            }),
            'middlename': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'e.g. Santos'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'e.g. Dela Cruz'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'e.g. 123456-ADM'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'e.g. juandelacruz@email.com'
            }),
            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                #'pattern': '09[0-9]{2} [0-9]{3} [0-9]{4}',
                'placeholder': 'e.g. 09123456789'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'id': '',
                'placeholder': 'Enter Password'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data


    def save(self, commit=True):

        user = super(UserSignupForm, self).save(commit=False)

        office_id = self.cleaned_data['office_id']

        # Fetch the corresponding Office instance
        office_instance = Office.objects.get(office_id=office_id)

        user.office_id = office_instance

        if commit:
            user.save()
        return user

