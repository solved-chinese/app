import os
from uuid import uuid4
import json

from django.db import models

from content.models import GeneralContentModel, \
    ReviewableMixin, AudioFile
from content.utils import validate_chinese_character_or_x
from content.data.makemeahanzi_dictionary import get_makemeahanzi_data


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.chinese:
        filename = f"{instance.chinese}#{instance.identifier}.{ext}"
    else:
        # set filename as random string
        filename = f'{uuid4().hex}.{ext}'
    return os.path.join('radical_images', filename)


class Radical(ReviewableMixin, GeneralContentModel):
    chinese = models.CharField(max_length=1,
                               validators=[validate_chinese_character_or_x])
    identifier = models.CharField(max_length=20, blank=True)

    image = models.ImageField(default='default.jpg',
                              upload_to=path_and_rename)
    pinyin = models.CharField(max_length=20, blank=True, default='TODO')
    audio = models.ForeignKey('AudioFile',
                              related_name='radicals',
                              related_query_name='radical',
                              null=True, blank=True,
                              on_delete=models.SET_NULL,)

    definition = models.CharField(max_length=100,
                                  blank=True, default='TODO')
    explanation = models.TextField(max_length=200,
                                   blank=True, default='TODO')

    class Meta:
        ordering = ['id']
        unique_together = ['chinese', 'identifier']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.fill_data()
        else:
            old_self = Radical.objects.get(pk=self.pk)
        if self._state.adding or \
                (self.pinyin and self.pinyin != old_self.pinyin):
            if not self.audio or self.audio.type != AudioFile.Type.CUSTOM:
                self.audio = AudioFile.get_by_pinyin(self.pinyin)
        super().save(*args, **kwargs)

    def fill_data(self):
        """ this fills necessary data from makemeahanzi,
        remember to save """
        if self.chinese == 'x':
            return
        characters_data = get_makemeahanzi_data()
        try:
            data = characters_data[self.chinese]
        except KeyError:
            self.add_warning("chinese field not in dictionary. Reference "
                             "the archived decomposition field to see if "
                             "there is a better alternative")
        else:
            self.archive = json.dumps(data, indent=4, ensure_ascii=False)

    def __str__(self):
        if self.identifier:
            return f"{self.chinese}({self.identifier})"
        else:
            return self.chinese

    def __repr__(self):
        id = self.id or -1
        return f"<R{id:04d}:{self.chinese}#{self.identifier}>"
