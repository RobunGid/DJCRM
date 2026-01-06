from django.urls import path

from notifications import views

app_name = "notifications"

urlpatterns = [
    path("message/update_status/<int:pk>", views.UpdateMessageStatus.as_view(), name="message_update_status"),
    path("team_invitation/update_status/<int:pk>", views.UpdateInvitationStatus.as_view(), name="team_invitation_update_status"),
]
