from django.urls import path

from rapidchat.users.views import user_detail_view, user_list_view, user_redirect_view, user_update_view

app_name = "users"
urlpatterns = [
    path("list/", view=user_list_view, name="users_list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
