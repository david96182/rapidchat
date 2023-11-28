from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from rapidchat.chats.models import Conversation

User = get_user_model()


class DRFChatsURLsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.user2 = User.objects.create(username="testuser2")
        self.conversation = Conversation.objects.create(name="testuser__testuser2")

    def test_conversation_detail(self):
        assert (
            reverse("api:conversation-detail", kwargs={"name": self.conversation.name})
            == f"/api/conversations/{self.conversation.name}/"
        )
        assert resolve(f"/api/conversations/{self.conversation.name}/").view_name == "api:conversation-detail"

    def test_conversation_list(self):
        assert reverse("api:conversation-list") == "/api/conversations/"
        assert resolve("/api/conversations/").view_name == "api:conversation-list"

    def test_messages_list(self):
        assert reverse("api:message-list") == "/api/messages/"
        assert resolve("/api/messages/").view_name == "api:message-list"
