from django.views.generic import UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse

from notifications.models import Message
from notifications.models import TeamInvitation

class UpdateMessageStatus(LoginRequiredMixin, UpdateView):
    fields = ("is_read",)
    model = Message
    success_url = reverse_lazy('dashboard:dashboard')
    
class UpdateInvitationStatus(LoginRequiredMixin, View):
    fields = ("status",)
    model = TeamInvitation
    success_url = reverse_lazy('dashboard:dashboard')
    
    def post(self, request, *args, **kwargs):
        team_invitation = TeamInvitation.objects.get(pk=kwargs["pk"])
        status = request.POST["action"]
        if status not in TeamInvitation.Status:
            return JsonResponse({"status": "fail"})

        team_invitation.status = status
        team_invitation.save()
        response = HttpResponse(status=302)
        response['Location'] = reverse_lazy("dashboard:dashboard")
        return response