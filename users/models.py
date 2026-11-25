from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя с авторизацией через email."""

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Телефон",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Статус сотрудника",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный пользователь",
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата регистрации",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email


class Payment(models.Model):
    """Модель платежа пользователя."""

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на счёт"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(
        verbose_name="Дата оплаты",
    )
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(course__isnull=False, lesson__isnull=True)
                    | models.Q(course__isnull=True, lesson__isnull=False)
                ),
                name="payment_course_or_lesson",
            ),
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="payment_positive_amount",
            ),
        ]

    def __str__(self):
        return f"{self.user.email}: {self.amount} руб."
