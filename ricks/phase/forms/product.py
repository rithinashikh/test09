from django import forms
from phase.models import Product
from django.forms import ModelForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'price','description','image','stock','category']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'price' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control','rows': 4}),
            'image' : forms.FileInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class':'form-control'}),

        }
        labels={
            'name':'Product Name',
            'price':'Price',
            'description':'Description',
            'image':'Image',
            'stock':'Stock',
            'category':'Category'
        }
