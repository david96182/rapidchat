from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from rapidchat.chats.models import Conversation

User = get_user_model()


class BaseChatView(LoginRequiredMixin, View):
    def get_conversations(self, request):
        # get conversations for user
        conversations = Conversation.objects.all()
        data = []

        for conversation in conversations:
            user1, user2 = conversation.name.split("__")
            conv_info = {}
            user = None
            if user1 == request.user.username:
                user = user2
            elif user2 == request.user.username:
                user = user1

            if user:
                messages = conversation.messages.all().order_by("-timestamp")
                if not messages.exists():
                    message = None
                else:
                    message = messages[0].content
                conv_info.update(
                    {
                        "user": user,
                        "name": conversation.name,
                        "last_message": message,
                    }
                )
                data.append(conv_info)

        return data


class ChatsListView(BaseChatView):
    def get(self, request, *args, **kwargs):
        return render(request, "chat/chats.html", {"conversations": self.get_conversations(request)})


chats_list_view = ChatsListView.as_view()


def error_404_view(request):
    return render(request, "404.html")


class ConversationView(BaseChatView):
    def get(self, request, *args, **kwargs):
        # Get the conversation name from the URL parameters
        conversation_name = kwargs.get("users")

        user1, user2 = conversation_name.split("__")
        if not User.objects.filter(username=user1).exists() or not User.objects.filter(username=user2).exists():
            return error_404_view(request)

        if request.user.username not in [user1, user2]:
            return error_404_view(request)

        conversation, created = Conversation.objects.get_or_create(name=conversation_name)

        # Get the other user in the conversation
        to_user = user1 if user2 == request.user.username else user2

        conversation = {"name": conversation_name, "user": to_user}

        # Render the conversation template with the conversation and other user
        return render(
            request,
            "chat/conversation.html",
            {
                "current_conversation": conversation,
                "to_user": to_user,
                "conversations": self.get_conversations(request),
            },
        )


conversation_view = ConversationView.as_view()
