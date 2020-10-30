from django.db import models

from jiezi.utils.mixins import StrDefaultReprMixin, CleanBeforeSaveMixin
from content.models import DFModelMixin


class CharacterSet(DFModelMixin, StrDefaultReprMixin, CleanBeforeSaveMixin,
                   models.Model):
    characters = models.ManyToManyField('Character')
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f'<cset{self.id}:{self.name} ' \
               f'{[repr(c) for c in self.characters.all()]}>'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for sctag in self.sc_tags.all():
            sctag.update_from_character_set() # FIXME make more efficient\
