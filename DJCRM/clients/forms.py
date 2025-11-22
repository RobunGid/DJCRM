from django import forms

from clients.models import Client, ClientComment

class AddClientForm(forms.ModelForm):
    class Meta:
        fields = ("name", "email", "description")
        model = Client
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter client name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter client email"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter client description"}),
		}

class AddClientCommentForm(forms.ModelForm):
    class Meta:
        model = ClientComment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter comment content", "style": "resize: none;"}),
		}