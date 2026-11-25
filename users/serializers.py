from rest_framework import serializers

from lms.serializers import CourseSerializer, LessonSerializer
from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа."""

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
        )


class PaymentDetailSerializer(PaymentSerializer):
    """Сериализатор платежа с вложенными данными."""

    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    payments = PaymentDetailSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payments",
        )
        read_only_fields = ("id", "payments")
