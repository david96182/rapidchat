from channels.db import database_sync_to_async
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthentication:
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the headers.
    """

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token

        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise AuthenticationFailed(_("User inactive or deleted."))

        return token.user


@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    # postpone model import to avoid ImproperlyConfigured error before Django
    # setup is complete.
    from django.contrib.auth.models import AnonymousUser

    if "token" not in scope:
        raise ValueError("Cannot find token in scope. You should wrap your consumer in " "TokenAuthMiddleware.")
    token = scope["token"]
    user = None
    try:
        auth = TokenAuthentication()
        user = auth.authenticate_credentials(token)
    except AuthenticationFailed:
        pass
    return user or AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware that takes a token from the query string and authenticates via Django Rest Framework authtoken.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from headers
        headers = dict(scope["headers"])
        cookies = headers[b"cookie"].decode()
        cookie_dict = {
            key.strip(): value.strip() for key, value in [cookie.split("=") for cookie in cookies.split(";")]
        }
        token = cookie_dict.get("auth_token", "")
        scope["token"] = token
        scope["user"] = await get_user(scope)
        return await self.app(scope, receive, send)
