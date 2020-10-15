from django.test import TestCase
from django.urls import reverse
from content.models import CharacterSet

from jiezi.tests.utils import create_student


class TestManageLibrary(TestCase):
    fixtures = ['content']

    def setUp(self):
        self.student = create_student()
        self.client.force_login(self.student.user)

    def test(self):
        response = self.client.get(reverse('character_set_list'))
        cset = CharacterSet.objects.first()
        self.assertContains(response, cset.name)
        response = self.client.post(reverse('student_character_tag_list'),
                                    {'character_set_id': cset.pk})
        self.assertEqual(response.status_code, 201) # 201_CREATED
        self.assertEqual(self.student.sc_tags.count(), 1)
        sc_tag = self.student.sc_tags.first()
        # test detail view
        response = self.client.get(reverse('student_character_tag_detail',
                                           args=[sc_tag.pk]))
        self.assertEqual(response.status_code, 200)
        # test manage_library view
        response = self.client.get(reverse('manage_library'))
        self.assertContains(response, sc_tag.name)
        # test manage_set view
        response = self.client.get(reverse('manage_library', args=[sc_tag.pk]))
        self.assertContains(response, sc_tag.name)
        # delete view
        response = self.client.delete(reverse('student_character_tag_detail',
                                              args=[sc_tag.pk]))
        self.assertEqual(response.status_code, 204)  # 204_NO_CONTENT
        self.assertEqual(self.student.sc_tags.count(), 0)
