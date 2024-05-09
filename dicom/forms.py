# dicom/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DICOMUploadForm(forms.Form):
    dicom_file = forms.FileField()
    
    
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
