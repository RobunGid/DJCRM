from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username", 
                                   widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your login"}))
    password = forms.CharField(label="Password", 
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"}))
    class Meta:
        model = get_user_model()
        fields = ("username", "password")
        
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your login"}))
    password1 = forms.CharField(label="Password", 
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"}))
    password2 = forms.CharField(label="Confirm password", 
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
        }
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email address"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"}),
        }
        required_fields = ("first_name", "last_name", "email")
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.required_fields:
            self.fields[field_name].required = True
     
    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already registered")
        return email
    
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'name': 'email'
        }))
    
class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
        