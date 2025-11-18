from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("add-lead/", views.AddLeadPage.as_view(), name="add_lead"),
]
