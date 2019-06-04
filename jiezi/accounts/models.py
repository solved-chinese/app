import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import learning.models  # to avoid cyclic import


class User(AbstractUser):
    # info
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255)
    # stats
    last_study_date = models.DateField()
    study_streak = models.IntegerField(default=0)
    last_study_duration = models.DurationField(default=datetime.timedelta(seconds=0))
    total_study_duration = models.DurationField(default=datetime.timedelta(seconds=0))

    def get_total_words_learned(self):
        return self.user_characters.filter(times_learned__gt=0).count()


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
        self.times_learned += 1
        self.time_last_learned = timezone.now()
        if ans != -1:
            if ans == 1:
                self.EF += 0.1;
            else:
                self.EF -= 0.8;
            if self.EF < 1.3:
                self.EF = 1.3
            if self.times_learned == 1:
                self.interval = 1
            elif self.times_learned == 2:
                self.interval = 6
            else:
                self.interval = (float)(self.interval) * self.EF
        self.save()

    def __str__(self):
        return f"<uc {self.pk}:{self.user}'s {self.character}>"

    class Meta:
        ordering = ['interval', 'time_added', 'character__pk']
        unique_together = ('user', 'character')


class UserCharacterTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_character_tags', related_query_name='user_character_tag')
    name = models.CharField(max_length=50)
    user_characters = models.ManyToManyField(UserCharacter, related_name='tags', related_query_name='tag')

    def __str__(self):
        return f"<uct {self.pk}:{self.user}'s {self.name}>"

    class Meta:
        unique_together = ('user', 'name')
