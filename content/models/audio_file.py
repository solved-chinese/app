from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class AudioFile(models.Model):
    class Origin(models.TextChoices):
        TAIWAN = 'taiwan', 'taiwan'
        SELF_RECORDED = 'self', 'self recorded'

    class Type(models.TextChoices):
        PINYIN = 'pinyin', 'pinyin'
        WORD = 'word', 'word'

    file = models.FileField(upload_to='audio')
    note = models.TextField(help_text="This is for internal use only, feel free "
                                      "to use it for note taking",
                            max_length=500, blank=True)
    content = models.TextField(max_length=300,
                               help_text="This field is used for searching")
    origin = models.CharField(max_length=10,
                              choices=Origin.choices,
                              default=Origin.SELF_RECORDED)
    type = models.CharField(max_length=10,
                            choices=Origin.choices)

    @classmethod
    def get_default_pk(cls):
        return cls.get_default().pk

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(file='default.mp3',
                                         content='default',
                                         origin='default')[0]

    @classmethod
    def get_by_pinyin(cls, pinyin):
        try:
            return cls.objects.filter(content=pinyin,
                                      type=cls.Type.PINYIN).get()
        except ObjectDoesNotExist:
            return cls.get_default()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<Audio{self.pk} {self.content}>"
