from django.test import TestCase
from django.urls import reverse
from content.models import CharacterSet

from jiezi.tests.utils import create_student
from ..learning_process import LearningProcess
from ..models import StudentCharacterTag


MAX_STEPS = 300

class TestLearningProcess(TestCase):
    """
    This tests the LearningProcess model
    """

    fixtures = ['content']

    def setUp(self):
        self.student = create_student()
        self.client.force_login(self.student.user)
        self.learning_process = LearningProcess.of(self.student)
        cset = CharacterSet.objects.first()
        self.sc_tag = StudentCharacterTag.objects.create(character_set=cset,
                                                    student=self.student)
        self.sc_tag.update_from_character_set()
        self.sc_tag.save()

    def test_perfect_learner(self):
        self.learning_process.start([self.sc_tag.pk])
        learning_set = set()
        review_set = set()
        for i in range(MAX_STEPS + 1):
            mode, a, b = self.learning_process.get_action()
            if mode is None:
                break
            elif mode == 'learn':
                learning_set.add(self.learning_process.character.pk)
            elif mode == 'review':
                review_set.add(self.learning_process.character.pk)
                self.learning_process.check_answer(
                    self.learning_process.review_answer_index)
        for sc in self.sc_tag.student_characters.all():
            self.assertSetEqual(learning_set, review_set)
            self.assertEqual(len(learning_set),
                             self.sc_tag.student_characters.count())
        self.assertLess(i, MAX_STEPS) # infinite loop

    def test_stupid_student(self):
        self.learning_process.start([self.sc_tag.pk])
        learning_set = set()
        review_set = set()
        for i in range(MAX_STEPS + 1):
            mode, a, b = self.learning_process.get_action()
            if mode is None:
                break
            elif mode == 'learn':
                learning_set.add(self.learning_process.character.pk)
            elif mode == 'review':
                review_set.add(self.learning_process.character.pk)
                self.learning_process.check_answer(-1)
        for sc in self.sc_tag.student_characters.all():
            self.assertSetEqual(learning_set, review_set)
            self.assertEqual(len(learning_set),
                             LearningProcess.MAX_SC_IN_PROGRESS_CNT)
        self.assertEqual(i, MAX_STEPS)  # infinite loop
