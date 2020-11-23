import uuid

from django.db import models


class Class(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE,
                                related_name='classes',
                                related_query_name='class')
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name="Class name")

    def notify_students(self, *args, **kwargs):
        for student in self.students.all():
            student.user.notify(*args, **kwargs)

    @property
    def student_count(self):
        return self.students.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('class_detail', args=[self.pk])

    @staticmethod
    def remove_testers(queryset):
        from accounts.models import User
        filter_kwargs = {f"teacher__user__{key}": value
            for key, value in User.REMOVE_TESTER_FILTER_KWARGS.items()}
        exclude_kwargs = {f"teacher__user__{key}": value
            for key, value in User.REMOVE_TESTER_EXCLUDE_KWARGS.items()}
        return queryset.filter(**filter_kwargs).exclude(**exclude_kwargs)

    def __str__(self):
        return f'Class: {self.name}'

    def __repr__(self):
        return f'<class {self.name} by {repr(self.teacher)}>'


