import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    """Фильтрация платежей."""

    class Meta:
        model = Payment
        fields = (
            "course",
            "lesson",
            "payment_method",
        )
