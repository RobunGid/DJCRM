from django.urls import path

from notifications import views

app_name = "notifications"

urlpatterns = [
    path("make-read/<int:pk>", views.UpdateNotificationStatus.as_view(), name="make_read"),
]
