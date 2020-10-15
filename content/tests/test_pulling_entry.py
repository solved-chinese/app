from django.test import TestCase, Client
from rest_framework.reverse import reverse

from accounts.models import User
from .. models import Character, Radical, CharacterSet


class TestEntryPull(TestCase):
    def test_pull_response(self):
        user = User.objects.create_superuser('superuser')
        client = Client()
        client.force_login(user)
        pull_response = client.get(reverse('update_entry'))
        self.assertEqual(pull_response.status_code, 200)
        html = pull_response.content.decode("utf-8")
        good_cnt = html.count('create') + html.count('update')
        bad_cnt = html.count('WARNING') + html.count('ERR')
        self.assertGreater(good_cnt + bad_cnt, 100)
        self.assertGreater(good_cnt, 100)
        self.assertGreater(Character.objects.count(), 10)
        self.assertGreater(Radical.objects.count(), 10)
        self.assertGreater(CharacterSet.objects.count(), 3)
