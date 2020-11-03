from django.test import TestCase

from learning.models import SCAbility, StudentCharacter, Ability
from content.models import Character
from jiezi.tests.utils import create_student


class TestManageLibrary(TestCase):
    fixtures = ['content']

    def setUp(self):
        self.student = create_student()
        self.client.force_login(self.student.user)

    def test_sc_creates_sca(self):
        character = Character.objects.first()
        sc = StudentCharacter.of(self.student, character)
        self.assertEqual(SCAbility.objects.count(),
                         Ability.objects.count())
        ability_set = set()
        for sca in SCAbility.objects.all():
            ability_set.add(sca.ability)
            self.assertEqual(sca.student, self.student)
            self.assertEqual(sca.character, character)
        self.assertEqual(len(ability_set),
                         Ability.objects.count())

    def test_sca_save_fills_sca_given_sc(self):
        character = Character.objects.first()
        sc = StudentCharacter.of(self.student, character)
        ability = Ability.objects.first()
        sca = SCAbility.of(sc, ability)
        self.assertEqual(sca.student_character, sc)
        self.assertEqual(sca.student, self.student)
        self.assertEqual(sca.character, character)

    def test_sca_save_fills_sca_given_s_c(self):
        character = Character.objects.first()
        sc = StudentCharacter.of(self.student, character)
        ability = Ability.objects.first()
        sca = SCAbility.of(sc.student, sc.character, ability)
        self.assertEqual(sca.student_character, sc)
        self.assertEqual(sca.student, self.student)
        self.assertEqual(sca.character, character)
