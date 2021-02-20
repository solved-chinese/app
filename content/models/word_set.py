from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from mptt.models import MPTTModel, TreeForeignKey

from content.models import GeneralContentModel, OrderableMixin


class WordInSet(OrderableMixin):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    word_set = models.ForeignKey('WordSet', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['word', 'word_set', 'order']


class WordSet(MPTTModel, GeneralContentModel):
    name = models.CharField(max_length=100, unique=True)
    jiezi_id = models.CharField(max_length=50, unique=True)
    words = models.ManyToManyField('Word', through='WordInSet',
                                   related_name='word_sets',
                                   related_query_name='word_set')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children',
                            related_query_name='child')

    class MPTTMeta:
        order_insertion_by = ['jiezi_id']

    class Meta:
        ordering = ['id']

    def clean(self):
        super().clean()
        if self.is_done:
            if self.is_leaf_node():
                if not self.words.exists():
                    raise ValidationError('leaf cannot be done without any word')
                for w in self.words.all():
                    if not w.is_done:
                        raise ValidationError(f"{w} not done")
            else:
                if self.words.exists():
                    raise ValidationError('non-leaf cannot be done with words')

    def render_all_words(self):
        return ', '.join(w.chinese for w in self.words.all())

    def reset_order(self):
        OrderableMixin.reset_order(self.wordinset_set)

    def get_absolute_url(self):
        return reverse('set_display', args=(self.pk,))

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        id = self.id or -1
        return f'<WS{id}:{self.name}>'
