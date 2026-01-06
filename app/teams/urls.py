from django.urls import path

from teams import views

app_name = "teams"

urlpatterns = [
    path("team-update/<int:pk>/", views.TeamUpdatePage.as_view(), name="team_update"),
    path("team-details/<int:pk>/", views.TeamDetailsPage.as_view(), name="team_details"),
    path("team-make-active/<int:pk>/", views.TeamActiveView.as_view(), name="team_make_active"),
    path("create-invitation/<int:pk>/", views.CreateInvitationView.as_view(), name="create_invitation"),
    path("team-invite/<int:team_pk>/<int:user_pk>/", views.TeamInviteView.as_view(), name="team_invite"),
    path("team-list/", views.TeamListPage.as_view(), name="team_list"),
]
