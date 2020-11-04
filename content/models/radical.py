from django.db import models

from jiezi.utils.mixins import StrDefaultReprMixin, CleanBeforeSaveMixin
from content.models import DFModelMixin


class Radical(DFModelMixin, StrDefaultReprMixin, CleanBeforeSaveMixin,
              models.Model):
    chinese = models.CharField(max_length=6)
    pinyin = models.CharField(max_length=15)
    definition = models.CharField(max_length=100)
    mnemonic_explanation = models.CharField(max_length=300, null=True, blank=True)
    mnemonic_image = models.ImageField(default='default.jpg')
    is_phonetic = models.BooleanField()
    is_semantic = models.BooleanField()

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return '<R' + '%04d' % self.id + ':' + self.chinese +'>'
