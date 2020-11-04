from django.db import models

from jiezi.utils.mixins import StrDefaultReprMixin, CleanBeforeSaveMixin
from content.models import DFModelMixin


class CharacterSet(DFModelMixin, StrDefaultReprMixin, CleanBeforeSaveMixin,
                   models.Model):
    characters = models.ManyToManyField('Character')
    name = models.CharField(max_length=50)

    def render_all_character(self):
        output = ''
        for c in self.characters.all():
            output += c.chinese
            output += ', '
        return output[:-2]

    def __str__(self):
        return f"{self.name}: {self.render_all_character()}"

    def __repr__(self):
        return f'<cset{self.id}:{self.name} ' \
               f'{[repr(c) for c in self.characters.all()]}>'
