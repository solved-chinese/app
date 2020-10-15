from django.test import TestCase
from django.urls import reverse


class TestGuest(TestCase):
    fixtures = ['content']

    def test(self):
        response = self.client.get(reverse('try_me'))
        self.assertRedirects(response, reverse('continue_learning'))
        user = response.wsgi_request.user
        self.assertTrue(user.is_guest)
        self.assertTrue(user.is_student)
        self.assertEqual(user.student.sc_tags.count(), 1)
