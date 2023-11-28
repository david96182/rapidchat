from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from rapidchat.chats.models import Conversation, Message
from rapidchat.chats.views import BaseChatView

User = get_user_model()


class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.conversation = Conversation.objects.create(name="user1__user2")
        self.conversation.join(self.user1)
        self.conversation.join(self.user2)
        self.message = Message.objects.create(
            conversation=self.conversation, from_user=self.user1, to_user=self.user2, content="Hello World"
        )

    def test_chats_list_view(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(reverse("chats:chats"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chats.html")

    def test_conversation_view(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(
            reverse("chats:conversation", args=[f"{self.user1.username}__{self.user2.username}"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/conversation.html")

    def test_get_conversations(self):
        request = self.factory.get("/")
        request.user = self.user1
        view = BaseChatView()
        view.setup(request)

        conversations = view.get_conversations(request)
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]["name"], self.conversation.name)

    def test_conversation_view_invalid_conversation_name(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(reverse("chats:conversation", args=["user5__user6"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "404.html")

    def test_conversation_view_invalid_user(self):
        self.client.login(username="invalid_user", password="pass")
        response = self.client.get(
            reverse("chats:conversation", args=[f"{self.user1.username}__{self.user2.username}"])
        )
        self.assertEqual(response.status_code, 302)

    def test_conversation_view_different_conversation_name_order(self):
        self.client.login(username="user1", password="pass")
        response = self.client.get(
            reverse("chats:conversation", args=[f"{self.user2.username}__{self.user1.username}"])
        )
        self.assertEqual(response.status_code, 302)
