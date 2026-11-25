from django.urls import path

from users.views import UserUpdateAPIView

app_name = "users"

urlpatterns = [
    path(
        "<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user_update",
    ),
]
