import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import learning.models  # to avoid cyclic import
from learning.learning_algorithm_constants import Constants


class User(AbstractUser):
    # info
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255)
    cn_level = models.CharField(max_length=15, default="Beginner")
    is_guest = models.BooleanField(null=True, default=False)
    # stats
    study_streak = models.IntegerField(default=0)
    last_study_time = models.DateTimeField(default=datetime.datetime.fromtimestamp(0))
    last_study_duration = models.DurationField(default=datetime.timedelta(seconds=0))
    last_study_vocab_count = models.IntegerField(default=0)
    total_study_duration = models.DurationField(default=datetime.timedelta(seconds=0))

    def get_total_words_learned(self):
        return self.user_characters.filter(learned=True).count()

    def get_total_words_mastered(self):
        return self.user_characters.filter(mastered=True).count()
    
    def get_display_name(self):
        if self.is_guest:
            return 'Guest'
        elif self.first_name and self.first_name != 'None':
            return self.first_name
        else:
            return self.username


def user_character_factory():
    """
    this function adds the spaced-repetition related variables for every
    test_field specified by the Character model
    """
    class AbstractModel(models.Model):
        class Meta:
            abstract = True

    test_fields = learning.models.Character.TEST_FIELDS
    for test_field in test_fields:
        AbstractModel.add_to_class(test_field + '_in_a_row',
                                   models.IntegerField(default=0))
        AbstractModel.add_to_class(test_field + '_in_a_row_required',
            models.IntegerField(default=Constants.DEFAULT_IN_A_ROW_REQUIRED))
        AbstractModel.add_to_class(test_field + '_mastered',
                                   models.BooleanField(default=False))
        AbstractModel.add_to_class(test_field + '_time_last_studied',
            models.DateTimeField(default=timezone.now))
    return AbstractModel

class UserCharacter(user_character_factory()):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_characters',
                             related_query_name='user_character', null=True)
    character = models.ForeignKey(learning.models.Character, on_delete=models.CASCADE)
    time_added = models.DateField(auto_now_add=True)
    learned = models.BooleanField(default=False)
    mastered = models.BooleanField(default=False)

    def update(self, is_correct, field_name):
        """
        N (default: 2) correct answers in a row of a field masters this field
        incorrect answers increases N up to a maximum of 4
        mastering both pinyin and definition_1 masters the character
        """
        if is_correct:
            field_in_a_row = getattr(self, field_name + '_in_a_row') + 1
            setattr(self, field_name + '_in_a_row', field_in_a_row)
            if field_in_a_row == getattr(self, field_name + '_in_a_row_required'):
                setattr(self, field_name + '_mastered', True)
                self.mastered = self.pinyin_mastered and self.definition_1_mastered
        else: # answer incorrect
            setattr(self, field_name + '_in_a_row', 0)
            field_in_a_row_required = getattr(self, field_name + '_in_a_row_required')
            field_in_a_row_required = min(field_in_a_row_required + 1,
                                          Constants.MAX_IN_A_ROW_REQUIRED)
            setattr(self, field_name + '_in_a_row_required',
                    field_in_a_row_required)
        setattr(self, field_name + '_time_last_studied', timezone.now())
        self.save()

    def __repr__(self):
        return f"<uc {self.pk}:{self.user}'s {self.character}>"

    class Meta:
        ordering = ['mastered', 'definition_1_mastered', 'pinyin_mastered']
        unique_together = ('user', 'character')


class UserCharacterTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_character_tags',
                             related_query_name='user_character_tag')
    name = models.CharField(max_length=50)
    user_characters = models.ManyToManyField(UserCharacter,
                                             related_name='tags',
                                             related_query_name='tag')

    def __repr__(self):
        return f"<uct {self.pk}:{self.user}'s {self.name}>"

    class Meta:
        unique_together = ('user', 'name')

