from rest_framework.authtoken.models import Token


class CreateAuthTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_anonymous and not request.COOKIES.get("auth_token"):
            token, created = Token.objects.get_or_create(user=request.user)
            response.set_cookie(key="auth_token", value=token.key, httponly=True, secure=True, samesite="Strict")
        elif request.user.is_anonymous and request.COOKIES.get("auth_token"):
            response.delete_cookie("auth_token")

        return response
