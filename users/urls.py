from django.urls import path

from users.views import PaymentListAPIView, UserUpdateAPIView

app_name = "users"

urlpatterns = [
    path(
        "<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user_update",
    ),
    path(
        "payments/",
        PaymentListAPIView.as_view(),
        name="payment_list",
    ),
]
