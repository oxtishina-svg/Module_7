from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson


class CourseAPITests(APITestCase):
    """Тесты CRUD для курсов."""

    def setUp(self):
        self.course = Course.objects.create(
            title="Python",
            description="Курс по Python",
        )

        self.list_url = "/api/courses/"
        self.detail_url = f"/api/courses/{self.course.pk}/"

    def test_create_course(self):
        response = self.client.post(
            self.list_url,
            {
                "title": "Django",
                "description": "Курс по Django",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Course.objects.count(), 2)

    def test_list_courses(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

    def test_retrieve_course(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["title"], "Python")

    def test_update_course(self):
        response = self.client.put(
            self.detail_url,
            {
                "title": "Advanced Python",
                "description": "Продвинутый курс",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.course.refresh_from_db()

        self.assertEqual(self.course.title, "Advanced Python")

    def test_partial_update_course(self):
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated Python"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.course.refresh_from_db()

        self.assertEqual(self.course.title, "Updated Python")

    def test_delete_course(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())


class LessonAPITests(APITestCase):
    """Тесты CRUD для уроков."""

    def setUp(self):
        self.course = Course.objects.create(
            title="Python",
            description="Курс по Python",
        )

        self.lesson = Lesson.objects.create(
            title="Первый урок",
            description="Описание урока",
            video_url="https://example.com/video",
            course=self.course,
        )

        self.list_url = "/api/lessons/"
        self.create_url = "/api/lessons/create/"
        self.detail_url = f"/api/lessons/{self.lesson.pk}/"
        self.update_url = f"/api/lessons/{self.lesson.pk}/update/"
        self.delete_url = f"/api/lessons/{self.lesson.pk}/delete/"

    def test_create_lesson(self):
        response = self.client.post(
            self.create_url,
            {
                "title": "Второй урок",
                "description": "Описание второго урока",
                "video_url": "https://example.com/video/2",
                "course": self.course.pk,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["title"], "Первый урок")

    def test_update_lesson(self):
        response = self.client.put(
            self.update_url,
            {
                "title": "Обновлённый урок",
                "description": "Новое описание",
                "video_url": "https://example.com/new-video",
                "course": self.course.pk,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lesson.refresh_from_db()

        self.assertEqual(self.lesson.title, "Обновлённый урок")

    def test_partial_update_lesson(self):
        response = self.client.patch(
            self.update_url,
            {"title": "Новое название"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lesson.refresh_from_db()

        self.assertEqual(self.lesson.title, "Новое название")

    def test_delete_lesson(self):
        response = self.client.delete(self.delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_lesson_without_course(self):
        response = self.client.post(
            self.create_url,
            {
                "title": "Урок без курса",
                "description": "Описание",
                "video_url": "https://example.com/video",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_delete_course_with_lessons(self):
        lesson_id = self.lesson.pk

        self.course.delete()

        self.assertFalse(Lesson.objects.filter(pk=lesson_id).exists())
