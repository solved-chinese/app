from django.db import models
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from classroom.models import Student
from content.models import Character
from jiezi.utils.mixins import StrDefaultReprMixin
from ..models import ReviewAccuracyAbstractModel


class SCQuerySet(models.QuerySet):
    def get_states_count(self):
        d = {}
        for num, choice in StudentCharacter.STATE_CHOICES:
            d[choice] = self.filter(state=num).count()
        return d


class StudentCharacterManager(models.Manager):
    def __init__(self, student=None, sc_tags = None, cset=None, scas=None,
                 *args, **kwargs):
        self._student = student
        self._sc_tags = sc_tags
        self._cset = cset
        self._scas = scas
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = SCQuerySet(model=self.model, using=self._db)
        if self._student is not None:
            queryset = queryset.filter(student=self._student)
        if self._sc_tags is not None:
            queryset = queryset.filter(sc_tag__in=self._sc_tags)
        if self._cset is not None:
            queryset = queryset.filter(character__in=self._cset.characters.all())
        if self._scas is not None:
            queryset = queryset.filter(sca__in=self._scas)
        return queryset

    def get_states_count_dict(self):
        return self.get_queryset().get_states_count()

    @classmethod
    def of(cls, model, student=None, character=None, sc_tags=None,
           cset=None, scas=None):
        if student and character:
            return model.objects.get_or_create(student=student,
                                               character=character)[0]
        manager = cls(student=student, sc_tags=sc_tags, cset=cset, scas=scas)
        manager.model = model
        return manager


def factory_student_character_manager_of(*args, **kargs):
    return StudentCharacterManager.of(StudentCharacter, *args, **kargs)


class StudentCharacter(StrDefaultReprMixin, ReviewAccuracyAbstractModel):
    TO_LEARN = 10
    IN_PROGRESS = 20
    MASTERED = 30
    STATE_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (MASTERED, 'Mastered'),
        (TO_LEARN, 'To Learn'),
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

    def test_review_update(self, is_correct, save=True):
        # this should be called after SCA update
        self._test_review_update(is_correct)
        super().test_review_update(is_correct, save=save)

    def __repr__(self):
        return f"<sc {self.pk}:{self.student}'s {self.character}>"

    class Meta:
        unique_together = ('student', 'character')
