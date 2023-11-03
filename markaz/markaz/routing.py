from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from principle import consumers

application = ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),

        ])
    ),
})