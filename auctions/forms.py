from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"}))
    
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Choose unique username"
                }
            )
        )
        
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Email"
                }
            )
        )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Create strong password"
                }
            )
        )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Confirm your password"
                }
            )
        )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")




