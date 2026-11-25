from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm

from users.models import User


class CustomUserCreationForm(BaseUserCreationForm):
    """Форма создания пользователя."""

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования пользователя."""

    class Meta:
        model = User
        fields = "__all__"
