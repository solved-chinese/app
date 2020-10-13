from datetime import timedelta
import random

from django.utils import timezone
from django.db import models
from django.db.models import F, Max, DurationField, ExpressionWrapper

import learning.learning_process
from content.models import Character
import learning.models


class SCQuerySet(models.QuerySet):
    def get_to_review(self):
        global_max_weighted_duration = timedelta(seconds=0)
        scs_to_review = self.filter(
            state=learning.models.StudentCharacter.IN_PROGRESS)
        if not scs_to_review.exists():
            return None, None
        sc_to_review = None
        field_index_to_review = None
        for index, test_field in enumerate(Character.TEST_FIELDS):
            annotated = scs_to_review.annotate(
                weighted_duration=ExpressionWrapper(
                    (timezone.now() - F(test_field + '_time_last_studied'))
                    / (F(test_field + '_in_a_row') + 1)
                    + learning.learning_process.LearningProcess.ADDED_DURATION,
                        output_field=DurationField()
                )
            )
            local_max_weighted_duration = annotated.aggregate(
                Max('weighted_duration')
            )['weighted_duration__max']
            if local_max_weighted_duration > global_max_weighted_duration:
                sc_to_review = annotated.filter(
                    weighted_duration=local_max_weighted_duration).first()
                field_index_to_review = index
                global_max_weighted_duration = local_max_weighted_duration
        return sc_to_review, field_index_to_review

    def get_states_count(self):
        d = {}
        for num, choice in learning.models.StudentCharacter.STATE_CHOICES:
            d[choice] = self.filter(state=num).count()
        return d

class StudentCharacterManager(models.Manager):
    def __init__(self, student=None, sc_tags = None, cset=None,
                 *args, **kwargs):
        self._student = student
        self._sc_tags = sc_tags
        self._cset = cset
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = SCQuerySet(model=self.model, using=self._db)
        if self._student is not None:
            queryset = queryset.filter(student=self._student)
        if self._sc_tags is not None:
            queryset = queryset.filter(sc_tag__in=self._sc_tags)
        if self._cset is not None:
            queryset = queryset.filter(character__in=self._cset.characters.all())
        return queryset

    def generate_choices(self, character, field_name, num_choices=4):
        """
        :returns choices(int[num_choices]), ans_index(int)
        """
        sc = self.get_queryset().get(character=character)
        kwargs = {f'character__{field_name}__iexact':
                      getattr(sc.character, field_name)}
        query_set = self.get_queryset().exclude(pk=sc.pk).exclude(**kwargs)
        query_set = query_set\
            [:learning.learning_process.LearningProcess.MAX_RANDOM_CHOICES]
        choices = [getattr(sc.character, field_name)
                   for sc in random.sample(list(query_set), num_choices - 1)]
        ans_index = random.randint(0, num_choices - 1)
        choices.insert(ans_index, getattr(sc.character, field_name))
        return choices, ans_index

    def get_one_to_learn(self):
        return self.get_queryset().filter(state=
                learning.models.StudentCharacter.TO_LEARN).first()

    def get_all_in_progress(self):
        return self.get_queryset().filter(state=
                learning.models.StudentCharacter.IN_PROGRESS)

    def count_all_in_progress(self):
        return self.get_all_in_progress().count()

    def get_mastered_count(self):
        return self.get_queryset().filter(state=
            learning.models.StudentCharacter.MASTERED).count()

    def get_in_progress_count(self):
        return self.get_queryset().filter(state=
            learning.models.StudentCharacter.IN_PROGRESS).count()

    def get_states_count_dict(self):
        return self.get_queryset().get_states_count()

    def get_to_review(self):
        return self.get_queryset().get_to_review()

    @classmethod
    def of(cls, model, student=None, character=None, sc_tags=None, cset=None):
        if student and character:
            return model.objects.get_or_create(student=student,
                                               character=character)[0]
        manager = cls(student=student, sc_tags=sc_tags, cset=cset)
        manager.model = model
        return manager


def factory_student_character_manager_of(*args, **kargs):
    return StudentCharacterManager.of(learning.models.StudentCharacter,
                                      *args, **kargs)


class SCTagManager(models.Manager):
    def filter_by_pk(self, pk):
        if isinstance(pk, int):
            return self.get_queryset().filter(pk=pk)
        return self.get_queryset().filter(pk__in=pk)
