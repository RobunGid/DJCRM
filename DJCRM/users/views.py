from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect

from users.forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from teams.models import Team
from users.models import Userprofile

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
        
        Userprofile.objects.create(user=form.instance, active_team=team)
        
        return super().form_valid(form)
    
class UserProfileOwn(LoginRequiredMixin, TemplateView):
    template_name = "users/own_profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["joined_teams"] = Team.objects.filter(members__in=[self.request.user]).all()
        return context
    
class UserProfile(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["joined_teams"] = Team.objects.filter(members__in=[self.object]).all()
        return context
    
    def get(self, request, *args, **kwargs):
        if self.request.user == self.get_object():
            return redirect("users:own_profile")
        return super().get(request, *args, **kwargs)
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    title = "Password change"
