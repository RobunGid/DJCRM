from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("add-lead/", views.AddLeadPage.as_view(), name="lead_add"),
    path("lead-list/", views.LeadListPage.as_view(), name="lead_list"),
    path("lead-details/<int:pk>/", views.LeadDetailsPage.as_view(), name="lead_details"),
    path("lead-update/<int:pk>/", views.LeadUpdatePage.as_view(), name="lead_update"),
    path("lead-delete/<int:pk>/", views.LeadDeletePage.as_view(), name="lead_delete"),
    path("lead-convert/<int:pk>/", views.LeadConvertToClient.as_view(), name="lead_convert_to_client"),
]
