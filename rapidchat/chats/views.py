from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class ChatsListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "chat/chats.html")


chats_list_view = ChatsListView.as_view()
