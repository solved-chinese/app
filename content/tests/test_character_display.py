from django.test import TestCase, Client
from rest_framework.reverse import reverse

from accounts.models import User
from .. models import Character, Radical, CharacterSet


class TestCharacterDisplay(TestCase):
    fixtures = ['content']

    def test_character_display(self):
        character = Character.objects.first()
        response = self.client.get(reverse('display_character',
                                           args=[character.pk]))
        self.assertContains(response, character.chinese)
        self.assertContains(response, character.pinyin)
        self.assertContains(response, character.definition_1)
