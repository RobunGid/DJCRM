from django.urls import path

from teams import views

app_name = "teams"

urlpatterns = [
    path("team-update/<int:pk>/", views.TeamUpdatePage.as_view(), name="team_update"),
    path("team-details/<int:pk>/", views.TeamDetailsPage.as_view(), name="team_details"),
    path("team-list/", views.TeamListPage.as_view(), name="team_list"),
]
