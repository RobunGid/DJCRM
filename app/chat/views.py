from django.contrib.auth.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from chat.models import Message
from teams.models import Team

class UserChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat/user_chat.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sender"] = self.request.user
        context["chat_messages"] = Message.objects.filter(
            Q(sender=self.request.user) & Q(receiver__pk=self.kwargs["user_pk"]) |
            Q(sender__pk=self.kwargs["user_pk"]) & Q(receiver=self.request.user)
            )
        return context
    
class TeamChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat/team_chat.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sender"] = self.request.user
        context["team_name"] = Team.objects.get(pk=self.kwargs["team_pk"]).name
        context["chat_messages"] = Message.objects.filter(
        	Q(team__pk=self.kwargs["team_pk"])
            )
        return context
    