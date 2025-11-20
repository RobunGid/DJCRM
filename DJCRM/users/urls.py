from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import path, reverse_lazy
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegister.as_view(), name="register"),
    path("profile/", views.UserProfile.as_view(), name="profile"),
]
