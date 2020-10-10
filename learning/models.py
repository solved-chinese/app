from django.db import models
from django.utils import timezone

from content.models import Character, CharacterSet
from accounts.models import User
from classroom.models import Student
from jiezi.utils.mixins import StrDefaultReprMixin
import learning.learning_process as learning_process
from learning.managers import StudentCharacterManager, \
    factory_student_character_manager_of


class Report(models.Model, StrDefaultReprMixin):
    user = models.ForeignKey('accounts.User', null=True,
                             on_delete=models.SET_NULL)
    origin = models.CharField(max_length=100)
    description_1 = models.CharField(max_length=100)
    description_2 = models.TextField()

    def __repr__(self):
        return f'<Report on {self.origin}: {self.description_1}>'

    class Meta:
        ordering = ['origin']


def student_character_factory():
    """
    this function adds the spaced-repetition related variables for every
    test_field specified by the Character model
    """
    class AbstractModel(models.Model):
        class Meta:
            abstract = True

    for test_field in Character.TEST_FIELDS:
        AbstractModel.add_to_class(test_field + '_in_a_row',
                                   models.IntegerField(default=0))
        AbstractModel.add_to_class(test_field + '_in_a_row_required',
            models.IntegerField(default=
            learning_process.LearningProcess.DEFAULT_IN_A_ROW_REQUIRED))
        AbstractModel.add_to_class(test_field + '_mastered',
                                   models.BooleanField(default=False))
        AbstractModel.add_to_class(test_field + '_time_last_studied',
            models.DateTimeField(auto_now_add=True))
    return AbstractModel


class StudentCharacter(student_character_factory(), StrDefaultReprMixin):
    TO_LEARN = 10
    IN_PROGRESS = 20
    MASTERED = 30
    STATE_CHOICES = [
        (TO_LEARN, 'To Learn'),
        (IN_PROGRESS, 'In Progress'),
        (MASTERED, 'Mastered'),
    ]
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES,
                                             default=TO_LEARN)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='student_characters',
                                related_query_name='student_character')
    character = models.ForeignKey(Character, on_delete=models.CASCADE,
                                  related_name='student_characters',
                                  related_query_name='student_character')
    time_added = models.DateField(auto_now_add=True)
    of = factory_student_character_manager_of
    objects = StudentCharacterManager()

    def update(self, is_correct, field_name):
        """
        N (default: 2) correct answers in a row of a field masters this field
        incorrect answers increases N up to a maximum of 4
        mastering all TEST_FIELDS masters the character
        """
        if is_correct:
            field_in_a_row = getattr(self, field_name + '_in_a_row') + 1
            setattr(self, field_name + '_in_a_row', field_in_a_row)
            if field_in_a_row == \
                    getattr(self, field_name + '_in_a_row_required'):
                setattr(self, field_name + '_mastered', True)
                self.mastered = all(getattr(self, f'{test_field}_mastered')
                                    for test_field in Character.TEST_FIELDS)
        else: # answer incorrect
            setattr(self, field_name + '_in_a_row', 0)
            field_in_a_row_required = \
                getattr(self, field_name + '_in_a_row_required')
            field_in_a_row_required = min(field_in_a_row_required + 1,
                learning_process.LearningProcess.MAX_IN_A_ROW_REQUIRED)
            setattr(self, field_name + '_in_a_row_required',
                    field_in_a_row_required)
        setattr(self, field_name + '_time_last_studied', timezone.now())
        self.save()

    def __repr__(self):
        return f"<sc {self.pk}:{self.student}'s {self.character}>"

    class Meta:
        # for effectively selecting random choices from mastered scs
        ordering = ['-state']
        unique_together = ('student', 'character')


class StudentCharacterTag(models.Model):
    character_set = models.ForeignKey(CharacterSet,
                                      on_delete=models.CASCADE,
                                      related_name='sc_tags',
                                      related_query_name='sc_tag')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='sc_tags',
                                related_query_name='sc_tag')
    student_characters = models.ManyToManyField(StudentCharacter,
                                                related_name='sc_tags',
                                                related_query_name='sc_tag')

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
            scs.append(self.student.student_characters.get_or_create(
                student=self.student, character=character)[0])
        self.student_characters.set(scs)

    def __str__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set.name}>"

    def __repr__(self):
        return f"<sct {self.pk}:{self.student}'s {self.character_set}>"

    class Meta:
        unique_together = ('student', 'character_set')
