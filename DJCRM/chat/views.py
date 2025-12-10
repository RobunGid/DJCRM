from django.contrib.auth.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import SafeString

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat/chat.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sender"] = SafeString({
            "username": self.request.user.username
        })
        return context
    