from django.db import models
from django.contrib.auth.models import AbstractUser
import learning.models  # to avoid cyclic import


class User(AbstractUser):
    raw_password = models.CharField(
        max_length=128,
        default='THIS_IS_NOT_RECORDED',
        help_text='A read-only field to record password only for development.'
    )


class UserCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_characters',
                             related_query_name='user_character', null=True)
    character = models.ForeignKey(learning.models.Character, on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.__str__() + ', ' + self.character.__str__()

    class Meta:
        ordering=['time_added']
        unique_together=(('user','character'),)


class UserCharacterTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_character_tags',
                             related_query_name='user_character_tag', null=True)
    user_characters = models.ManyToManyField(UserCharacter, related_name='tags', related_query_name='tag')
    # limit the choice
    name = models.CharField(max_length=50)
    is_filtered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__() + ',' + self.name

    class Meta:
        unique_together = (('user', 'name'),)

    class SameNameException(Exception):
        pass
