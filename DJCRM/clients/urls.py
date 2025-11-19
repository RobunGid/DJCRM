from django.urls import path

from clients import views

app_name = "clients"

urlpatterns = [
    path("client-list/", views.ClientListPage.as_view(), name="client_list"),
	path("client-details/<int:pk>/", views.ClientDetailsPage.as_view(), name="client_details"),
	path("client-delete/<int:pk>/", views.ClientDeletePage.as_view(), name="client_delete"),
	path("client-update/<int:pk>/", views.ClientUpdatePage.as_view(), name="client_update"),
	path("client-add/", views.ClientAddPage.as_view(), name="client_add"),
]
