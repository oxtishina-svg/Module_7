from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = "lms"

router = DefaultRouter()

router.register(
    r"courses",
    CourseViewSet,
    basename="course",
)

urlpatterns = [
    path(
        "lessons/",
        LessonListAPIView.as_view(),
        name="lesson_list",
    ),
    path(
        "lessons/create/",
        LessonCreateAPIView.as_view(),
        name="lesson_create",
    ),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_detail",
    ),
    path(
        "lessons/<int:pk>/update/",
        LessonUpdateAPIView.as_view(),
        name="lesson_update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lesson_delete",
    ),
]

urlpatterns += router.urls
