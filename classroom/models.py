from datetime import timedelta
import uuid

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

    def quit_class(self, class_object):
        self.in_class = None
        self.save()

    @property
    def display_name(self):
        return self.user.get_display_name()

    @property
    def total_study_duration_seconds(self):
        return self.total_study_duration.total_seconds()

    def __repr__(self):
        return f"<student of {self.user}>"


class Teacher(StrDefaultReprMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='teacher')
    school = models.CharField(max_length=200, blank=True,
        help_text="""Please also include the region / country. For example,
                "St. Mark's School, Massachusetts, United States" """)
    school_description = models.TextField(max_length=2000, blank=True,
        verbose_name="Please describe your school",
        help_text="""You may include the curriculum that your school uses
        (E.g. Integrated Chinese, IB curriculum, HSK Standard Course, etc.
        ) """)
    wechat_id = models.CharField(max_length=40, blank=True,
                                 help_text="Optional, if applicable")

    @property
    def display_name(self):
        return self.user.get_display_name()

    def __repr__(self):
        return f"<teacher {self.display_name}>"


class Class(StrDefaultReprMixin, models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name='classes',
                                related_query_name='class')
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100)

    @property
    def student_count(self):
        return self.students.count()

    def __repr__(self):
        return f'class {self.name} by teacher {self.teacher.display_name}'
