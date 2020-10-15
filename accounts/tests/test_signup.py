from django.test import TestCase
from rest_framework.reverse import reverse


class TestUserSignup(TestCase):
    def test_signup_student_get(self):
        response = self.client.get(reverse('student_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_teacher_get(self):
        response = self.client.get(reverse('teacher_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_student_post(self):
        response = self.client.post(
            reverse('student_signup'),
            {
                'username': 'test_student',
                'password1': 'test_password',
                'password2': 'test_password',
                'email': 'test_student@g.com',
                'display_name': 'Student Test',
            }
        )
        user = response.wsgi_request.user
        self.assertTrue(user.is_student)
        self.assertRedirects(response, reverse('index'))

    def test_signup_teacher_post(self):
        response = self.client.post(
            reverse('teacher_signup'),
            {
                'username': 'test_teacher',
                'password1': 'test_password',
                'password2': 'test_password',
                'email': 'test_teacher@g.com',
                'display_name': 'Mr. Teacher',
            }
        )
        user = response.wsgi_request.user
        self.assertTrue(user.is_teacher)
        self.assertRedirects(response, reverse('index'))
