from django.db import models
from django.utils.crypto import get_random_string


# alphanumeric chars with misleading chars like 1&I, 0&O removed
CODE_ALLOWED_CHARS = 'ABCDEFGHJKLMNPQRSTVWXYZ23456789'


class Class(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE,
                                related_name='classes',
                                related_query_name='class')
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=100, verbose_name="Class name")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['teacher', 'name']

    def save(self, **kwargs):
        if self._state.adding:
            if not self.code:
                self.code = get_random_string(
                    4, allowed_chars=CODE_ALLOWED_CHARS)
        super().save(**kwargs)

    @property
    def student_count(self):
        return self.students.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('class_detail', args=[self.pk])

    def __str__(self):
        return f'Class {self.name}'

    def __repr__(self):
        return f'<class {self.name} by {repr(self.teacher)}>'


