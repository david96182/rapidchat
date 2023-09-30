from django.urls import path

from rapidchat.chats.views import chat_view

app_name = "chats"
urlpatterns = [
    path("chat/", view=chat_view, name="chat"),
]
