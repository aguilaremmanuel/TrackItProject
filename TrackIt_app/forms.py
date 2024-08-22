from django import forms
from .models import *
from django.core.exceptions import ValidationError

class UserSignupForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': '', 
            'id': '',
            'placeholder': '',
        })
    )

    class Meta:
        model = User
        fields = ['lastname', 'firstname', 'middlename', 'email', 'contact_no', 'password']

        widgets = {
            'lastname': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
            'firstname': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
            'middlename': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
            'email': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
            'contact_no': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
            'password': forms.TextInput(attrs={
                'class': '',
                'id': '',
                'placeholder': ''
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
    


