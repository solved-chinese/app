from django.db import models


class AudioFile(models.Model):
    class Origin(models.TextChoices):
        TAIWAN = 'taiwan', 'taiwan'
        SELF_RECORDED = 'self', 'self recorded'

    file = models.FileField(upload_to='audio')
    note = models.TextField(help_text="This is for internal use only, feel free "
                                      "to use it for note taking",
                            max_length=500, blank=True)
    content = models.TextField(max_length=300,
                               help_text="This field is used for searching")
    origin = models.CharField(max_length=10,
                              choices=Origin.choices,
                              default=Origin.SELF_RECORDED)

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(file='default.mp3',
                                         content='default',
                                         origin='default')[0]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<Audio{self.pk} {self.content}>"
