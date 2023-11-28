from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class UrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

    def test_chats_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("chats:chats"))
        self.assertEqual(response.status_code, 200)

    def test_conversation_view(self):
        self.client.login(username="testuser", password="testpass")
        user2 = get_user_model().objects.create_user(username="testuser2", password="testpass")
        response = self.client.get(
            reverse("chats:conversation", args=[{"users": f"{self.user.username}__{user2.username}"}])
        )
        self.assertEqual(response.status_code, 200)
