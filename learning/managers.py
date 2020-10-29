from django.db import models

import learning.models
import learning.models.student_character


class SCQuerySet(models.QuerySet):
    def get_states_count(self):
        d = {}
        for num, choice in learning.models.student_character.StudentCharacter.STATE_CHOICES:
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
    return StudentCharacterManager.of(
        learning.models.student_character.StudentCharacter,
        *args, **kargs)


class SCTagManager(models.Manager):
    def filter_by_pk(self, pk):
        if isinstance(pk, int):
            return self.get_queryset().filter(pk=pk)
        return self.get_queryset().filter(pk__in=pk)
