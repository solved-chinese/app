from django.test import TestCase
from django.urls import reverse

from .utils import create_student, create_teacher


class TestIndex(TestCase):
    def test_anonymous_user(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'unauthenticated_index.html')
        self.assertEqual(response.status_code, 200)

    def test_teacher(self):
        teacher = create_teacher()
        self.client.force_login(teacher.user)
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'teacher_index.html')
        self.assertEqual(response.status_code, 200)

    def test_student(self):
        student = create_student()
        self.client.force_login(student.user)
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'student_index.html')
        self.assertEqual(response.status_code, 200)