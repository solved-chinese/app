from django.test import TestCase, Client
from rest_framework.reverse import reverse

from .. models import Character


class TestSearch(TestCase):
    fixtures = ['content']

    def test_search(self):
        character = Character.objects.first()
        response = self.client.post(reverse('search'),
                                    {'keyword': character.chinese})
        self.assertContains(response, character.chinese)
        response = self.client.post(reverse('search'),
                                    {'keyword': character.pinyin})
        self.assertContains(response, character.chinese)
