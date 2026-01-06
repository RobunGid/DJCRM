from django import forms

from teams.models import Team

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        fields = ("name",)
        model = Team
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter team name"}),
		}