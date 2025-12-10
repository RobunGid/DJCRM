from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<user_pk>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
