from django.db import models

from learning.models import ReviewManager


class Assignment(models.Model):
    in_class = models.ForeignKey('Class', on_delete=models.CASCADE,
                                 related_name='assignments',
                                 related_query_name='assignment')
    character_set = models.ForeignKey('content.CharacterSet',
                                      on_delete=models.CASCADE,
                                      related_name='assignments',
                                      related_query_name='assignment')
    review_manager = models.ForeignKey('learning.ReviewManager',
                                       on_delete=models.PROTECT,
                                       related_name='+',
                                       default=ReviewManager.get_default_pk)
    published_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_modified_time']
        unique_together = ['in_class', 'character_set']

    def save(self, *args, **kwargs):
        is_adding = self._state.adding
        super().save(*args, **kwargs)
        if is_adding:
            self.in_class.notify_students(
                f'An new assignment "{self.name}" has been published.')

    @property
    def name(self):
        return self.character_set.name

    def __str__(self):
        return f'Assignment in {self.in_class}'

    def __repr__(self):
        return f'<Assignment in {repr(self.in_class)}>'
