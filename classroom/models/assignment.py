from django.db import models


from content.models import OrderableMixin


class WordInAssignment(OrderableMixin):
    word = models.ForeignKey('content.Word', on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['word', 'assignment', 'order']


class CharacterInAssignment(OrderableMixin):
    character = models.ForeignKey('content.Character', on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['character', 'assignment', 'order']


class RadicalInAssignment(OrderableMixin):
    radical = models.ForeignKey('content.Radical', on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['radical', 'assignment', 'order']


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    klass = models.ForeignKey('Class', on_delete=models.CASCADE,
                              related_name='assignments',
                              related_query_name='assignment')
    words = models.ManyToManyField('content.Word',
                                   through='WordInAssignment')
    characters = models.ManyToManyField('content.Character',
                                        through='CharacterInAssignment')
    radicals = models.ManyToManyField('content.Radical',
                                      through='RadicalInAssignment')
    published_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['-last_modified_time']
        unique_together = ['klass', 'name']

    def __str__(self):
        return f'Assignment: {self.name}'

    def __repr__(self):
        return f'<Assignment {self.name} in {repr(self.klass)}>'
