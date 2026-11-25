from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройки административной панели курсов."""

    list_display = ("id", "title")
    search_fields = ("title", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Настройки административной панели уроков."""

    list_display = ("id", "title", "course")
    list_filter = ("course",)
    search_fields = ("title", "description")
