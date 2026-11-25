from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import Payment, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "city",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "city",
                    "avatar",
                ),
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Важные даты",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_date",
        "course",
        "lesson",
        "amount",
        "payment_method",
    )

    list_filter = (
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "user__email",
        "course__title",
        "lesson__title",
    )

    ordering = ("-payment_date",)
