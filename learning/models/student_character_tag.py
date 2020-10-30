from django.db import models

from classroom.models import Student
from content.models import CharacterSet
from learning.models import StudentCharacter


class SCTagManager(models.Manager):
    def filter_by_pk(self, pk):
        if isinstance(pk, int):
            return self.get_queryset().filter(pk=pk)
        return self.get_queryset().filter(pk__in=pk)


class StudentCharacterTag(models.Model):
    """
    This class connects a student with a character set. It syncs the changes
    from CharacterSet.
    """
    character_set = models.ForeignKey(CharacterSet,
                                      on_delete=models.CASCADE,
                                      related_name='sc_tags',
                                      related_query_name='sc_tag')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='sc_tags',
                                related_query_name='sc_tag')
    student_characters = models.ManyToManyField(StudentCharacter,
                                                related_name='sc_tags',
                                                related_query_name='sc_tag')
    objects = SCTagManager()

    def update_from_character_set(self):
        """
        This method ensures that the relationship between this StudentCharacterTag
        and its UserCharacters follows that between its CharacterSet and the
        corresponding Characters
        TODO: auto update though sparingly
        solution 1: add a lazy tag attribute and call this method lazily
        solution 2: in addition to solution 1, call this only when
        character_set gets updated
        """
        scs = []
        for character in self.character_set.characters.all():
            scs.append(StudentCharacter.of(self.student, character))
        self.student_characters.set(scs)

    @property
    def states_count(self):
        return self.student_characters.all().get_states_count()

    @property
    def name(self):
        return self.character_set.name

    def __str__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set.name}>"

    def __repr__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set}>"

    class Meta:
        unique_together = ('student', 'character_set')