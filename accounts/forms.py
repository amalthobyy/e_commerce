from django import  forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError

class UserSignup(forms.ModelForm):
    password =forms.CharField(widget= forms.PasswordInput)
    confirm_password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model= User
        fields = ['first_name','last_name','email','password']


    def clean_email(self):
        email =self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")   
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password
    

class Emailauthentication(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class OtpForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='OTP')


    





