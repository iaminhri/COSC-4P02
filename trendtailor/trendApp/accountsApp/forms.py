from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, ProfileImage

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True, widget=forms.
                EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.
                TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.
                TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Username', 'autofocus': True}
    ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Password'}
    ))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'phone_number', 'bio', 'street_address', 'city', 'province', 'postal_code', 'birth_date']
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }