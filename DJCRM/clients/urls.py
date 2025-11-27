from django.urls import path

from clients import views

app_name = "clients"

urlpatterns = [
    path("client-list/", views.ClientListPage.as_view(), name="client_list"),
	path("client-details/<int:pk>/", views.ClientDetailsPage.as_view(), name="client_details"),
	path("client-delete/<int:pk>/", views.ClientDeletePage.as_view(), name="client_delete"),
	path("client-update/<int:pk>/", views.ClientUpdatePage.as_view(), name="client_update"),
	path("client-add/", views.ClientAddPage.as_view(), name="client_add"),
    path("client-add-comment/<int:pk>/", views.ClientCommentAddView.as_view(), name="client_add_comment"),
    path("client-add-file/<int:pk>/", views.ClientFileAddView.as_view(), name="client_add_file"),
	path("client-delete-comment/<int:pk>/", views.ClientCommentDeleteView.as_view(), name="client_delete_comment"),
    path("client-delete-file/<int:pk>/", views.ClientFileDeleteView.as_view(), name="client_delete_file"),
    path("client-export/csv/", views.ClientExportCSVView.as_view(), name="client_export_csv"),
]
