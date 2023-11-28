from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from rapidchat.chats.models import Conversation, Message

User = get_user_model()


class ConversationViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user2 = User.objects.create(username="testuser2")
        self.conversation = Conversation.objects.create(name="testuser__testuser2")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_conversations(self):
        url = reverse("api:conversation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_conversation(self):
        url = reverse("api:conversation-detail", args=[self.conversation.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MessageViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user2 = User.objects.create(username="testuser2")
        self.conversation = Conversation.objects.create(name="testuser__testuser2")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.message = Message.objects.create(
            conversation=self.conversation, from_user=self.user, to_user=self.user2, content="Hello World"
        )

    def test_list_messages(self):
        url = reverse("api:message-list")
        params = {"conversation": self.conversation.name}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
