from django.db import models


class Course(models.Model):
    """Модель учебного курса."""

    title = models.CharField(
        max_length=255,
        verbose_name="Название курса",
    )

    preview = models.ImageField(
        upload_to="courses/previews/",
        blank=True,
        null=True,
        verbose_name="Превью курса",
    )

    description = models.TextField(
        verbose_name="Описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=255,
        verbose_name="Название урока",
    )

    description = models.TextField(
        verbose_name="Описание урока",
    )

    preview = models.ImageField(
        upload_to="lessons/previews/",
        blank=True,
        null=True,
        verbose_name="Превью урока",
    )

    video_url = models.URLField(
        max_length=500,
        verbose_name="Ссылка на видео",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]

    def __str__(self):
        return self.title
