from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("add-lead/", views.AddLeadPage.as_view(), name="add_lead"),
    path("lead-list/", views.LeadListPage.as_view(), name="lead_list"),
    path("lead-details/<int:pk>/", views.LeadDetailsPage.as_view(), name="lead_details"),
]
