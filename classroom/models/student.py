from datetime import timedelta

from django.db import models

from accounts.models import User
from jiezi.utils.mixins import StrDefaultReprMixin


class Student(StrDefaultReprMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='student')
    in_class = models.ForeignKey('classroom.Class', on_delete=models.SET_NULL,
                                 related_name='students',
                                 related_query_name='student',
                                 null=True, blank=True)
    total_study_duration = models.DurationField(default=timedelta(0))

    def update_duration(self, delta_time):
        self.total_study_duration += delta_time
        self.save()

    def join_class(self, class_object):
        assert self.in_class is None, \
            f"You can't join a class while already in a class ({self.in_class})"
        self.in_class = class_object
        self.save()

    def quit_class(self):
        self.in_class = None
        self.save()

    @property
    def display_name(self):
        return self.user.display_name

    @property
    def total_study_duration_seconds(self):
        return self.total_study_duration.total_seconds()

    def __repr__(self):
        return f"<student of {self.user}>"

    @classmethod
    def of(cls, user):
        """convenient get_or_create"""
        return cls.objects.get_or_create(user=user)[0]
