from django import forms
from .models import Supplier, Material


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_person", "phone", "email"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "sku", "category", "supplier", "quantity", "reorder_level", "unit_cost"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_cost": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }