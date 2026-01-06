from django.contrib.auth.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import SafeString
from django.db.models import Q

from chat.models import Message

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat/chat.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sender"] = SafeString({
            "username": self.request.user.username
        })
        context["chat_messages"] = Message.objects.filter(
            Q(sender=self.request.user) & Q(receiver__pk=self.kwargs["user_pk"])
            |
            Q(sender__pk=self.kwargs["user_pk"]) & Q(receiver=self.request.user)
            
            )
        return context
    