from django.urls import path

from rapidchat.chats.views import chats_list_view

app_name = "chats"
urlpatterns = [
    path("list/", view=chats_list_view, name="chats"),
]
