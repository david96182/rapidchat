from django.urls import path

from rapidchat.chats.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path("chat/<conversation_name>/", ChatConsumer.as_asgi()),
    path("notifications/", NotificationConsumer.as_asgi()),
]
