from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создаёт тестовые данные для проверки платежей."

    @transaction.atomic
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="student@example.com",
            defaults={
                "first_name": "Test",
                "last_name": "Student",
                "city": "Saint Petersburg",
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        course, _ = Course.objects.get_or_create(
            title="Python Backend",
            defaults={
                "description": "Учебный курс по Python.",
            },
        )

        lesson, _ = Lesson.objects.get_or_create(
            title="Основы Django REST Framework",
            course=course,
            defaults={
                "description": "Введение в Django REST Framework.",
                "video_url": "https://example.com/video/1",
            },
        )

        now = timezone.now()

        payments = [
            {
                "user": user,
                "course": course,
                "lesson": None,
                "amount": Decimal("15000.00"),
                "payment_method": Payment.PaymentMethod.TRANSFER,
                "payment_date": now - timedelta(days=10),
            },
            {
                "user": user,
                "course": None,
                "lesson": lesson,
                "amount": Decimal("2500.00"),
                "payment_method": Payment.PaymentMethod.CASH,
                "payment_date": now - timedelta(days=5),
            },
            {
                "user": user,
                "course": None,
                "lesson": lesson,
                "amount": Decimal("3000.00"),
                "payment_method": Payment.PaymentMethod.TRANSFER,
                "payment_date": now - timedelta(days=1),
            },
        ]

        created_count = 0

        for payment_data in payments:
            payment_date = payment_data.pop("payment_date")

            _, created = Payment.objects.get_or_create(
                **payment_data,
                defaults={
                    "payment_date": payment_date,
                },
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Создано платежей: {created_count}"))

        self.stdout.write(f"ID пользователя: {user.pk}")
        self.stdout.write(f"ID курса: {course.pk}")
        self.stdout.write(f"ID урока: {lesson.pk}")
