from datetime import timedelta
import uuid

from django.db import models

from accounts.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='student')
    in_class = models.ForeignKey('classroom.Class', on_delete=models.SET_NULL,
                                 related_name='students',
                                 related_query_name='student',
                                 null=True, blank=True)
    total_study_duration = models.DurationField(default=timedelta(0))

    @property
    def display_name(self):
        return self.user.get_display_name()

    def update_duration(self, delta_time):
        self.total_study_duration += delta_time
        self.save()

    @property
    def total_study_duration_seconds(self):
        return self.total_study_duration.total_seconds()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='teacher')


class Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name='classes',
                                related_query_name='class')
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100)

    @property
    def student_count(self):
        return self.students.count()
