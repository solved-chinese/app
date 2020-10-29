from django.db import models

from classroom.models import Student
from content.models import CharacterSet
from learning.managers import SCTagManager
from learning.models import StudentCharacter


class StudentCharacterTag(models.Model):
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
        TODO: It should be called sparingly for efficiency reasons.
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