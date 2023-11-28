from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from rapidchat.chats.middleware import TokenAuthentication


class TokenAuthenticationTests(TestCase):
    def setUp(self):
        self.authentication = TokenAuthentication()
        self.user = self.create_user()
        self.token = self.create_token(self.user)

    def create_user(self):
        User = get_user_model()
        return User.objects.create_user(username="testuser", password="testpassword")

    def create_token(self, user):
        return Token.objects.create(user=user)

    def test_valid_token(self):
        user = self.authentication.authenticate_credentials(self.token.key)
        self.assertEqual(user, self.user)

    def test_invalid_token(self):
        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate_credentials("invalid_token")

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        with self.assertRaises(AuthenticationFailed):
            self.authentication.authenticate_credentials(self.token.key)
