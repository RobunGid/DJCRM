from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<user_pk>\d+)/$', consumers.ChatConsumerPersonal.as_asgi()),
    re_path(r'^ws/team_chat/(?P<user_pk>\d+)/$', consumers.ChatConsumerTeam.as_asgi()),
]
