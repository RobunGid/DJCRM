from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from users.forms import LoginUserForm, RegisterUserForm
from teams.models import Team

# Create your views here.
class UserLogin(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Authorization"}
    
class UserRegister(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Register"}
    success_url = reverse_lazy("users:login")
    
    def form_valid(self, form):
        form.instance.save()
        team = Team.objects.create(name=f"{form.cleaned_data["username"]}'s team", created_by=form.instance)
        team.members.add(form.instance.id)
        team.save()
        return super().form_valid(form)
    
    
class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    