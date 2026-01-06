from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, ListView, View, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from core.utils import DataMixin
from teams.models import Team
from teams.forms import TeamUpdateForm
from notifications.models import TeamInvitation

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
    
class TeamActiveView(DataMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        team = Team.objects.filter(members__in=[request.user]).get(pk=kwargs["pk"])
        userprofile = request.user.userprofile
        userprofile.active_team = team
        userprofile.save()
        
        return redirect("teams:team_details", pk=kwargs["pk"])
    
User = get_user_model()
    
class CreateInvitationView(LoginRequiredMixin, TemplateView):
    template_name = "teams/create_invitation.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.get(pk=kwargs["pk"])
        if "q" in self.request.GET:
            value = self.request.GET["q"]
            context["users"] = User.objects.filter(
                Q(first_name__contains=value) |
                Q(last_name__contains=value) |
                Q(username__contains=value) |
                Q(email__contains=value) &
                Q(pk__ne=self.request.user.pk)
            ).values("pk", "first_name", "email", "last_name", "username")
        return context
    
class TeamInviteView(View):
    def post(self, request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs["team_pk"])
        user = User.objects.get(pk=kwargs["user_pk"])
        TeamInvitation.objects.create(team=team, receiver=user)
        return HttpResponse({"status": "success"})