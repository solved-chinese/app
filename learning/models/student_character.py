from django.db import models
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from classroom.models import Student
from content.models import Character
from jiezi.utils.mixins import StrDefaultReprMixin
from learning.managers import factory_student_character_manager_of, \
    StudentCharacterManager


class StudentCharacter(models.Model, StrDefaultReprMixin):
    TO_LEARN = 10
    IN_PROGRESS = 20
    MASTERED = 30
    STATE_CHOICES = [
        (TO_LEARN, 'To Learn'),
        (IN_PROGRESS, 'In Progress'),
        (MASTERED, 'Mastered'),
    ]
    state = FSMIntegerField(choices=STATE_CHOICES, default=TO_LEARN)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='student_characters',
                                related_query_name='student_character')
    character = models.ForeignKey(Character, on_delete=models.CASCADE,
                                  related_name='student_characters',
                                  related_query_name='student_character')
    time_added = models.DateField(auto_now_add=True)
    time_last_studied = models.DateTimeField(auto_now=True)

    of = factory_student_character_manager_of
    objects = StudentCharacterManager()

    @transition(state, source="*", target=RETURN_VALUE(IN_PROGRESS, MASTERED))
    def _learn_update(self):
        if self.state == self.MASTERED:
            return self.MASTERED
        else:
            return self.IN_PROGRESS

    def learn_update(self):
        self._learn_update()
        self.save()

    @transition(state, source=(IN_PROGRESS, MASTERED),
                target=RETURN_VALUE(IN_PROGRESS, MASTERED))
    def _test_review_update(self, is_correct):
        from learning.models import SCAbility, Ability
        if is_correct \
            and all(SCAbility.of(self, ability).state == SCAbility.MASTERED
                    for ability in Ability.objects.all()):
            return self.MASTERED
        return self.IN_PROGRESS

    def test_review_update(self, is_correct):
        # this should be called after SCA update
        self._test_review_update(is_correct)
        self.save()

    def __repr__(self):
        return f"<sc {self.pk}:{self.student}'s {self.character}>"

    class Meta:
        unique_together = ('student', 'character')