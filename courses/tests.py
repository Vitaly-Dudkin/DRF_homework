from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User


# Create your tests here.
class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='john',
            password='john_snow',
            is_staff=True,
            is_superuser=False
        )

        self.course = Course.objects.create(
            name='test course',
            description='just for a test course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='test lesson',
            description='just for a test lesson',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        response = self.client.get(
            reverse('courses:list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [
                {
                    "id": 1,
                    "name": self.lesson.name,
                    "owner": self.lesson.owner.pk,
                    "description": self.lesson.description,
                    'course': self.lesson.course.pk,
                    "preview": None,
                    "video": None

                }
            ]
        )

    def test_retrieve_lesson(self):
        response = self.client.get(
            reverse('courses:detail', args=[self.lesson.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        data = {
            "id": 1,
            "name": self.lesson.name,
            "owner": self.lesson.owner.pk,
            "description": self.lesson.description,
            'course': self.lesson.course.pk,
        }

        response = self.client.post(
            reverse('courses:create'),
            data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            reverse('courses:delete', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_update_lesson(self):
        update_data = {
            "id": 1,
            "name": "update_name",
            "owner": self.lesson.owner.pk,
            "description": "update_description",
            'course': self.lesson.course.pk,
        }

        response = self.client.put(
            reverse("courses:update", args=[self.lesson.pk]),
            data=update_data
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        pass
