from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson


class CourseSerializerTestCase(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title="Python Backend",
            description="Тестовый курс",
        )

        self.lesson_one = Lesson.objects.create(
            title="Первый урок",
            description="Описание первого урока",
            video_url="https://example.com/video/1",
            course=self.course,
        )

        self.lesson_two = Lesson.objects.create(
            title="Второй урок",
            description="Описание второго урока",
            video_url="https://example.com/video/2",
            course=self.course,
        )

    def test_lessons_count(self):
        response = self.client.get(
            f"/api/courses/{self.course.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lessons_count"], 2)

    def test_nested_lessons(self):
        response = self.client.get(
            f"/api/courses/{self.course.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("lessons", response.data)
        self.assertEqual(len(response.data["lessons"]), 2)

        lesson_ids = {lesson["id"] for lesson in response.data["lessons"]}

        self.assertEqual(
            lesson_ids,
            {
                self.lesson_one.pk,
                self.lesson_two.pk,
            },
        )

    def test_course_without_lessons(self):
        empty_course = Course.objects.create(
            title="Пустой курс",
            description="Курс без уроков",
        )

        response = self.client.get(
            f"/api/courses/{empty_course.pk}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lessons_count"], 0)
        self.assertEqual(response.data["lessons"], [])
