from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.utils import DataMixin
from leads.models import Lead
from clients.models import Client
from teams.models import Team

class Dashboard(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    def get_context_data(self, **kwargs):
        team = Team.objects.filter(created_by=self.request.user).first()
        clients = Client.objects.filter(team=team).order_by("-created_at")[:5]
        leads = Lead.objects.filter(team=team, converted_to_client=False).order_by("-created_at")[:5]
        context = super().get_context_data(**kwargs)
        context["leads"] = leads
        context["clients"] = clients
        return context
    