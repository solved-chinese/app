from django.db import models


class Assignment(models.Model):
    klass = models.ForeignKey('Class', on_delete=models.CASCADE,
                              related_name='assignments',
                              related_query_name='assignment')
    wordset = models.ForeignKey('content.WordSet',
                                on_delete=models.CASCADE,
                                related_name='assignments',
                                related_query_name='assignment')
    published_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_modified_time']
        unique_together = ['klass', 'wordset']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('assignment_detail', args=[self.pk])

    @property
    def name(self):
        return self.wordset.name

    def get_stats(self):
        return {}

    def __str__(self):
        return f'Assignment: {self.name}'

    def __repr__(self):
        return f'<Assignment {self.name} in {repr(self.klass)}>'
