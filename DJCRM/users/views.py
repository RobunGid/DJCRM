from django.contrib.admin.sites import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView

from users.forms import LoginUserForm, RegisterUserForm

# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Authorization"}
    
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Register"}
    success_url = reverse_lazy("users:login")