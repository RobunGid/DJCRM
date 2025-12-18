from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from notifications.forms import NotificationUpdateForm
from notifications.models import Notification

class UpdateNotificationStatus(LoginRequiredMixin, UpdateView):
    form_class = NotificationUpdateForm
    model = Notification
    success_url = reverse_lazy('dashboard:dashboard')