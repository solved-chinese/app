import os
from uuid import uuid4

from django.db import models

from content.models import GeneralContentModel


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.chinese:
        filename = f"{repr(instance)}.{ext}"
    else:
        # set filename as random string
        filename = f'{uuid4().hex}.{ext}'
    return os.path.join('radical_images', filename)


class Radical(GeneralContentModel):
    chinese = models.CharField(max_length=1)
    identifier = models.CharField(max_length=20, blank=True)

    image = models.ImageField(default='default.jpg',
                              upload_to=path_and_rename)
    pinyin = models.CharField(max_length=20, blank=True, default='TODO')

    definition = models.CharField(max_length=100,
                                  blank=True, default='TODO')
    explanation = models.TextField(max_length=200,
                                   blank=True, default='TODO')

    class Meta:
        unique_together = ['chinese', 'identifier']

    def __str__(self):
        if self.identifier:
            return f"{self.chinese}({self.identifier})"
        else:
            return self.chinese

    def __repr__(self):
        return f"<R{self.id:04d}:{self.chinese}#{self.identifier}>"
