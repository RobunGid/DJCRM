from django import forms

from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        fields = ("name", "email", "description", "priority", "status")
        model = Lead
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter lead name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter lead email"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter lead description"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
		}