from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path("user/<int:user_pk>/", views.ChatView.as_view(), name="chat")
]
