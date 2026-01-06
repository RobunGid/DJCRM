from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path("user/<int:user_pk>/", views.UserChatView.as_view(), name="user_chat"),
    path("team/<int:team_pk>/", views.TeamChatView.as_view(), name="team_chat"),
]
