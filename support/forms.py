from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Claim

class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'is_customer', 'is_admin']  

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['title','website_link', 'description']     