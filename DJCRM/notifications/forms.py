from django import forms
from notifications.models import Notification

class NotificationUpdateForm(forms.ModelForm):
    class Meta:
        fields = ("is_read",)
        model = Notification