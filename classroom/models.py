import datetime

from django.db import models

from accounts.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='student')

    study_streak = models.IntegerField(default=0)
    last_study_time = models.DateTimeField(auto_now_add=True)
    last_study_duration = models.DurationField(
        default=datetime.timedelta(seconds=0))
    last_study_vocab_count = models.IntegerField(default=0)
    total_study_duration = models.DurationField(
        default=datetime.timedelta(seconds=0))

    def start_learning_update(self):
        pass

    def continue_learning_update(self):
        pass


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='teacher')
