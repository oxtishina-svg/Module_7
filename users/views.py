from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой."""

    queryset = Payment.objects.select_related(
        "user",
        "course",
        "lesson",
    )
    serializer_class = PaymentSerializer

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )

    filterset_class = PaymentFilter
    ordering_fields = ("payment_date",)
    ordering = ("-payment_date",)
