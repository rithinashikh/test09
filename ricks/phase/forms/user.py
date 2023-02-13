from django import forms
from phase.models import UserDetail, Address
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

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name","housename", "locality", "phone", "city", "state", "zipcode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'housename': forms.TextInput(attrs={'class': 'form-control'}),
            "locality": forms.TextInput(attrs={'class': 'form-control'}),
            "city": forms.TextInput(attrs={'class': 'form-control'}),
            "state": forms.Select(attrs={'class': 'form-control'}),
            "zipcode": forms.NumberInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels={
            'name':'Name',
            'housename':'House no.',
            'locality':'Locality',
            'city':'City',
            'state':'State',
            'zipcode':'Zipcode',
            'phone':'Phone',
        }
        # label_attrs = {
        #     'name': {'class': 'text-black'},
        #     'housename': {'class': 'text-black'},
        #     'locality': {'class': 'text-black'},
        #     'city': {'class': 'text-black'},
        #     'state': {'class': 'text-black'},
        #     'zipcode': {'class': 'text-black'},
        #     'phone': {'class': 'text-black'},
        # }
        