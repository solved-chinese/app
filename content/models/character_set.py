from django.db import models

from jiezi.utils.mixins import StrDefaultReprMixin, CleanBeforeSaveMixin
from content.models import DFModelMixin


class CharacterSet(DFModelMixin, StrDefaultReprMixin, CleanBeforeSaveMixin,
                   models.Model):
    characters = models.ManyToManyField('Character')
    name = models.CharField(max_length=50)

    def __str__(self):
        label = f"{self.name}: "
        for c in self.characters.all():
            label += c.chinese
            label += ','
        return label[:-1]

    def __repr__(self):
        return f'<cset{self.id}:{self.name} ' \
               f'{[repr(c) for c in self.characters.all()]}>'
