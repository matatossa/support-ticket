from django import forms
from .models import Account ,UserProfile

from django import forms
from .models import Account, UserProfile

class RegisterationFrom(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    
    # Role choices
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['Phone_number', 'email', 'password', 'role']

    def __init__(self, *args, **kwargs):
        super(RegisterationFrom, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input100'

    def clean(self):
        cleaned_data = super(RegisterationFrom, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('repeat_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('role' ,'Phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
