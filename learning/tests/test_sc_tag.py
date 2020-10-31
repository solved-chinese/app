from django.test import TestCase

from learning.models import StudentCharacter, StudentCharacterTag
from content.models import CharacterSet, Character
from jiezi.tests.utils import create_student


class TestSCTag(TestCase):
    fixtures = ['content']

    def setUp(self):
        self.student = create_student()
        self.client.force_login(self.student.user)

    def test_cset_update_updates_sctag(self):
        cset = CharacterSet.objects.first()
        sc_tag = StudentCharacterTag.objects.create(student=self.student,
                                                    character_set=cset)
        self.assertFalse(sc_tag.is_updated)
        sc_tag.check_update()
        self.assertTrue(sc_tag.is_updated)
        for c in cset.characters.all():
            self.assertTrue(StudentCharacter.objects.filter(
                character=c, student=self.student).exists())
        c = Character.objects.exclude(characterset=cset).first()
        cset.characters.set([c])
        sc_tag.refresh_from_db()
        self.assertFalse(sc_tag.is_updated)
        sc_tag.check_update()
        self.assertTrue(sc_tag.is_updated)
        self.assertTrue(StudentCharacter.objects.filter(
                character=c, student=self.student).exists())
