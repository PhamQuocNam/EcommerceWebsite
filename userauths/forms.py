from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget= forms.EmailInput(attrs={"placeholder":"Email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    address= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}))
    city= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "City"}))
    country= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Country"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2','address','city','country','phone']