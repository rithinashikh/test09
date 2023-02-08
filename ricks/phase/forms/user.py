from django import forms
from phase.models import UserDetail
from django.forms import ModelForm

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uname', 'uemail','uphone','upassword']
        widgets = {
            'uname' : forms.TextInput(attrs={'class':'form-control'}),
            'uemail' : forms.EmailInput(attrs={'class':'form-control'}),
            'uphone' : forms.NumberInput(attrs={'class':'form-control'}),
            'upassword' : forms.PasswordInput(attrs={'class':'form-control'}),
        }
        labels={
            'uname':'User Name',
            'uemail':'Email',
            'uphone':'Phone no',
            'upassword':'Password',
        }

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['uname','upassword']
        widgets = {
            'uname' : forms.TextInput(attrs={'class':'form-control'}),
            'upassword' : forms.PasswordInput(attrs={'class':'form-control'}),
        }
        labels={
            'uname':'User Name',
            'upassword':'Password',
        }