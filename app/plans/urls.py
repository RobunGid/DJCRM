from django.urls import path

from plans import views 

app_name = "plans"

urlpatterns = [
    path("plan-list/", views.PlanListPage.as_view(), name="plan_list"),
    path("plan-details/<int:pk>/", views.PlanDetailsPage.as_view(), name="plan_details"),
]
