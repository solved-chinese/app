from django.db import models
from django.db.models import ExpressionWrapper, F, DurationField, Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from learning.models.ability import Ability
from learning.constants import *
from learning.models import StudentCharacter


class SCAbilityQuerySet(models.QuerySet):
    def get_to_review(self):
        sc_abilities_to_review = self.filter(state=SCAbility.IN_PROGRESS)
        if not sc_abilities_to_review.exists():
            return None
        annotated = sc_abilities_to_review.annotate(
            weighted_duration=ExpressionWrapper(
                (timezone.now() - F('time_last_studied'))
                  / (F('in_a_row') + 1)
                + (timezone.now() - F('student_character__time_last_studied'))
                  / MAX_IN_A_ROW_REQUIRED
                + ADDED_DURATION,
                output_field=DurationField()
            )
        )
        max_weighted_duration = annotated.aggregate(
            Max('weighted_duration')
        )['weighted_duration__max']
        return annotated.filter(
            weighted_duration=max_weighted_duration).first()

    def learn_update(self):
        for sca in self.all():
            sca.learn_update()


class SCAbilityManager(models.Manager):
    def get_queryset(self):
        queryset = SCAbilityQuerySet(model=self.model, using=self._db)
        return queryset

    def create_sc_ability_from_sc(self, sc):
        """
        This is called from creation signal of StudentCharacter
        """
        for ability in Ability.objects.all():
            self.create(student_character=sc, ability=ability)


class SCAbility(models.Model):
    TO_LEARN = 10
    IN_PROGRESS = 20
    MASTERED = 30
    STATE_CHOICES = [
        (TO_LEARN, 'To Learn'),
        (IN_PROGRESS, 'In Progress'),
        (MASTERED, 'Mastered'),
    ]
    state = FSMIntegerField(choices=STATE_CHOICES, default=TO_LEARN)
    # (student, character) pair or student_character will be filled after
    # creation from post_save signal
    student = models.ForeignKey('classroom.Student', null=True,
                                on_delete=models.CASCADE,
                                related_name='scas', related_query_name='sca')
    character = models.ForeignKey('content.Character', null=True,
                                  on_delete=models.CASCADE,
                                  related_name='scas', related_query_name='sca')
    student_character = models.ForeignKey('StudentCharacter', null=True,
                                          on_delete=models.CASCADE,
                                          related_name='scas',
                                          related_query_name='sca')
    ability = models.ForeignKey('Ability', on_delete=models.CASCADE,
                                related_name='scas', related_query_name='sca')

    in_a_row = models.IntegerField(default=0)
    in_a_row_required = models.IntegerField(
        default=DEFAULT_IN_A_ROW_REQUIRED)
    time_last_studied = models.DateTimeField(auto_now=True)

    objects = SCAbilityManager()

    class Meta:
        unique_together = ('student', 'character', 'ability')

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
        # currently once ability mastered, it would never change
        # because answering incorrectly later
        if self.state == self.MASTERED:
            return self.MASTERED
        if is_correct:
            self.in_a_row += 1
            if self.in_a_row == self.in_a_row_required:
                return self.MASTERED
        else: # incorrect
            self.in_a_row = 0
            self.in_a_row_required = max(self.in_a_row_required + 1,
                                         self.max_in_a_row_requied)
        return self.IN_PROGRESS

    def test_review_update(self, is_correct):
        self._test_review_update(is_correct)
        self.save()

    @classmethod
    def of(cls, *args):
        if len(args) == 2:
            return cls.objects.get(student_character=args[0], ability=args[1])
        elif len(args) == 3:
            return cls.objects.get(student=args[0], character=args[1],
                                   ability=args[2])
        else:
            raise ValueError(f"Should be 2 or 3 args but get {len(args)}")

    def save(self, *args, **kwargs):
        if self._state.adding:
            assert self.student_character is not None \
                   or (self.student is not None and self.character is not None), \
                   '(student, character) pair must not be None'
            if self.student_character is None:
                self.student_character = StudentCharacter.of(
                    self.student, self.character)
            else:
                self.student = self.student_character.student
                self.character = self.student_character.character
            self.in_a_row_required = self.default_in_a_row_required
        super().save(*args, **kwargs)

    @property
    def max_in_a_row_requied(self):
        return self.ability.max_in_a_row_requied

    @property
    def default_in_a_row_required(self):
        return self.ability.default_in_a_row_required


@receiver(post_save, sender=StudentCharacter)
def create_scas_from_sc_creation(sender, instance, created, **kwargs):
    if created:
        SCAbility.objects.create_sc_ability_from_sc(instance)
