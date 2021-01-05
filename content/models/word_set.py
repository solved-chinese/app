from django.db import models
from django.core.exceptions import ValidationError

from content.models import GeneralContentModel, OrderableMixin


class WordInSet(OrderableMixin):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    word_set = models.ForeignKey('WordSet', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['word', 'word_set', 'order']


class WordSet(GeneralContentModel):
    name = models.CharField(max_length=30, unique=True)
    words = models.ManyToManyField('Word', through='WordInSet',
                                   related_name='word_sets',
                                   related_query_name='word_set')

    class Meta:
        ordering = ['id']

    def clean(self):
        super().clean()
        if self.is_done:
            if not self.words.exists():
                raise ValidationError('cannot be done without any word')
            for w in self.words.all():
                if not w.is_done:
                    raise ValidationError(f"{w} not done")

    def render_all_words(self):
        output = ''
        for w in self.words.all():
            output += w.chinese
            output += ', '
        return output[:-2]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def reset_order(self):
        OrderableMixin.reset_order(self.wordinset_set)

    def __str__(self):
        return f"{self.name}: {self.render_all_words()}"

    def __repr__(self):
        return f'<WS{self.id}:{self.name} ' \
               f'{[repr(c) for c in self.words.all()]}>'
