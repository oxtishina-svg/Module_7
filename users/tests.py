from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):
    """Тесты пользователей и редактирования профиля."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="TestPassword123!",
            first_name="Test",
        )

        self.url = f"/api/users/{self.user.pk}/"

    def test_create_user(self):
        self.assertEqual(self.user.email, "user@example.com")

        self.assertTrue(self.user.check_password("TestPassword123!"))

        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123!",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_authentication_by_email(self):
        user = authenticate(
            email="user@example.com",
            password="TestPassword123!",
        )

        self.assertEqual(user, self.user)

    def test_retrieve_user_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            self.user.email,
        )

        self.assertNotIn("password", response.data)

    def test_update_user_profile(self):
        response = self.client.patch(
            self.url,
            {
                "city": "Manchester",
                "phone": "+441234567890",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertEqual(self.user.city, "Manchester")
        self.assertEqual(self.user.phone, "+441234567890")

    def test_cannot_change_admin_permissions(self):
        response = self.client.patch(
            self.url,
            {
                "is_staff": True,
                "is_superuser": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
