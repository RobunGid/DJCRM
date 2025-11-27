from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("add-lead/", views.LeadAddPage.as_view(), name="lead_add"),
    path("lead-list/", views.LeadListPage.as_view(), name="lead_list"),
    path("lead-details/<int:pk>/", views.LeadDetailsPage.as_view(), name="lead_details"),
    path("lead-update/<int:pk>/", views.LeadUpdatePage.as_view(), name="lead_update"),
    path("lead-delete/<int:pk>/", views.LeadDeletePage.as_view(), name="lead_delete"),
    path("lead-convert/<int:pk>/", views.LeadConvertToClientPage.as_view(), name="lead_convert_to_client"),
    path("lead-add-comment/<int:pk>/", views.LeadCommentAddView.as_view(), name="lead_add_comment"),
    path("lead-delete-comment/<int:pk>/", views.LeadCommentDeleteView.as_view(), name="lead_delete_comment"),
    path("lead-delete-file/<int:pk>/", views.LeadFileDeleteView.as_view(), name="lead_delete_file"),
    path("lead-add-file/<int:pk>/", views.LeadFileAddView.as_view(), name="lead_add_file"),
    path("lead-export/csv/", views.LeadExportCSVView.as_view(), name="lead_export_csv"),
]
