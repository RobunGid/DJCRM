from django import forms

from leads.models import Lead, LeadComment, LeadFile

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
        
class AddLeadCommentForm(forms.ModelForm):
    class Meta:
        model = LeadComment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter comment content", "style": "resize: none;"}),
		}
        
class AddLeadFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ("file", )