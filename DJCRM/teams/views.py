from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from core.utils import DataMixin
from teams.models import Team
from teams.forms import TeamUpdateForm

class TeamUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "teams/team_update.html"
    form_class = TeamUpdateForm
    extra_context = {"button_text": "Update"}
    title = None
    success_message = "Team was updated successfully"
    success_url = reverse_lazy("users:profile")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Team - ID #{self.object.pk}"
        return context
    
class TeamDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_details.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_object().name
        return context
    
class TeamListPage(DataMixin, LoginRequiredMixin, ListView):
    model = Team
    template_name = "teams/team_list.html"
    title = None
    context_object_name = "teams"
    
    def get_queryset(self):
        return Team.objects.filter(members__in=[self.request.user]).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    