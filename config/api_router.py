from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from rapidchat.chats.api.views import ConversationViewSet
from rapidchat.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("conversations", ConversationViewSet)


app_name = "api"
urlpatterns = router.urls
