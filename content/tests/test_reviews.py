from django.test import TestCase
from rest_framework.reverse import reverse

from ..reviews import AVAILABLE_REVIEW_TYPES
from jiezi.tests.utils import create_student
from ..models import Character


class TestLearningProcess(TestCase):
    fixtures = ['content']

    def setUp(self):
        self.student = create_student()
        self.user = self.student.user
        self.client.force_login(self.user)

    def test_review(self):
        character = Character.objects.first()
        for index, review_type in enumerate(AVAILABLE_REVIEW_TYPES):
            response = self.client.get(reverse('review_character',
                kwargs={'character_pk': character.pk, 'review_type': index}))
            self.assertEqual(response.status_code, 200)
            response = self.client.post(
                reverse('review_character',
                        kwargs={'character_pk': character.pk,
                                'review_type': index}),
                {'user_answer': "something"}
            )
            self.assertContains(response, 'correct_answer')
