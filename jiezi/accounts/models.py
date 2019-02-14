from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    time_added = models.DateField(auto_now_add=True)
    time_last_learned = models.DateTimeField(null=True)
    times_learned = models.IntegerField(default=0)
    EF = models.FloatField(default=2.5)
    interval = models.DecimalField(default=1, max_digits=7, decimal_places=2)

    # -1 first learn 0 wrong 1 correct
    def update(self, ans):
        self.times_learned+=1
        self.time_last_learned=timezone.now()
        if ans!=-1:
            if ans==1:
                self.EF+=0.1;
            else:
                self.EF-=0.8;
            if self.EF<1.3:
                self.EF=1.3
            if self.times_learned==1:
                self.interval=1
            elif self.times_learned==2:
                self.interval=6
            else:
                self.interval = (float)(self.interval)*self.EF
        self.save()

    def __str__(self):
        return self.user.__str__() + ', ' + self.character.__str__()

    class Meta:
        ordering=['interval','time_added','character__pk']
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
