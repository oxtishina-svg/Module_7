from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер пользователей с авторизацией через email."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт обычного пользователя."""

        if not email:
            raise ValueError("Необходимо указать email.")

        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт администратора."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Администратор должен иметь is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Администратор должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
