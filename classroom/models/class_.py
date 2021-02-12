import uuid

from django.db import models


class Class(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE,
                                related_name='classes',
                                related_query_name='class')
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100, verbose_name="Class name")
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def student_count(self):
        return self.students.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('class_detail', args=[self.pk])

    def __str__(self):
        return f'Class: {self.name}'

    def __repr__(self):
        return f'<class {self.name} by {repr(self.teacher)}>'


