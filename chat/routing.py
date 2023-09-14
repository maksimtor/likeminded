from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat_search/(?P<room_name>\w+)/$', consumers.ChatSearchConsumer.as_asgi())
]