from django import forms
from phase.models import Category
from django.forms import ModelForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
        }
        labels={
            'name':'Category Name',
        }