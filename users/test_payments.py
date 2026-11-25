from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import Payment, User


class PaymentAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="student@example.com",
            password="testpassword123",
        )

        self.course = Course.objects.create(
            title="Python Backend",
            description="Тестовый курс",
        )

        self.lesson = Lesson.objects.create(
            title="Django REST Framework",
            description="Тестовый урок",
            video_url="https://example.com/video",
            course=self.course,
        )

        now = timezone.now()

        self.course_payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount=Decimal("15000.00"),
            payment_method=Payment.PaymentMethod.TRANSFER,
            payment_date=now - timedelta(days=10),
        )

        self.cash_payment = Payment.objects.create(
            user=self.user,
            lesson=self.lesson,
            amount=Decimal("2500.00"),
            payment_method=Payment.PaymentMethod.CASH,
            payment_date=now - timedelta(days=5),
        )

        self.transfer_payment = Payment.objects.create(
            user=self.user,
            lesson=self.lesson,
            amount=Decimal("3000.00"),
            payment_method=Payment.PaymentMethod.TRANSFER,
            payment_date=now - timedelta(days=1),
        )

        self.url = "/api/users/payments/"

    def test_payment_list(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 3)

    def test_filter_by_course(self):
        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.course_payment.pk,
        )

    def test_filter_by_lesson(self):
        response = self.client.get(
            self.url,
            {"lesson": self.lesson.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_cash(self):
        response = self.client.get(
            self.url,
            {"payment_method": "cash"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.cash_payment.pk,
        )

    def test_filter_by_transfer(self):
        response = self.client.get(
            self.url,
            {"payment_method": "transfer"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ordering_ascending(self):
        response = self.client.get(
            self.url,
            {"ordering": "payment_date"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payment_ids = [payment["id"] for payment in response.data]

        self.assertEqual(
            payment_ids,
            [
                self.course_payment.pk,
                self.cash_payment.pk,
                self.transfer_payment.pk,
            ],
        )

    def test_ordering_descending(self):
        response = self.client.get(
            self.url,
            {"ordering": "-payment_date"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payment_ids = [payment["id"] for payment in response.data]

        self.assertEqual(
            payment_ids,
            [
                self.transfer_payment.pk,
                self.cash_payment.pk,
                self.course_payment.pk,
            ],
        )

    def test_combined_filters(self):
        response = self.client.get(
            self.url,
            {
                "lesson": self.lesson.pk,
                "payment_method": "transfer",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.transfer_payment.pk,
        )

    def test_invalid_course_filter(self):
        response = self.client.get(
            self.url,
            {"course": 999999},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_payment_history(self):
        response = self.client.get(
            f"/api/users/{self.user.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("payments", response.data)
        self.assertEqual(len(response.data["payments"]), 3)

        payments = {payment["id"]: payment for payment in response.data["payments"]}

        self.assertEqual(
            payments[self.course_payment.pk]["course"]["id"],
            self.course.pk,
        )

        self.assertEqual(
            payments[self.cash_payment.pk]["lesson"]["id"],
            self.lesson.pk,
        )
