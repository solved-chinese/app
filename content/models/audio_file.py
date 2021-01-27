import os
import json
import logging
from jiezi.settings import BASE_DIR

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class AudioFile(models.Model):
    class Origin(models.TextChoices):
        TAIWAN = 'taiwan', 'taiwan'
        BAIDU = 'baidu', 'baidu'
        SELF_RECORDED = 'self', 'self recorded'

    class Type(models.TextChoices):
        PINYIN = 'pinyin', 'pinyin'
        CUSTOM = 'custom', 'custom'
        WORD = 'word', 'word'

    file = models.FileField(upload_to='audio')
    note = models.TextField(help_text="This is for internal use only, feel free "
                                      "to use it for note taking",
                            max_length=500, blank=True)
    content = models.TextField(max_length=300, help_text="""
        This field is used for auto searching, and (type, content) must be unique. 
        When type is pinyin, content must be pinyin with tone without any 
        whitespace to either side. When type is word, content must be chinese 
        characters. If you don't want this audio to be matched to a content object 
        automatically, set type to custom. 
        """)
    origin = models.CharField(max_length=10,
                              choices=Origin.choices,
                              default=Origin.SELF_RECORDED)
    type = models.CharField(max_length=10,
                            choices=Type.choices)
    archive = models.TextField(help_text="This is auto-generated as reference. "
                                         "Read-only",
                               max_length=500, blank=True)

    class Meta:
        ordering = ('id',)
        unique_together = ('type', 'content')

    @classmethod
    def get_default_pk(cls):
        return cls.get_default().pk

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(file='default.mp3',
                                         content='default',
                                         origin='default')[0]

    @classmethod
    def get_by_chinese(cls, chinese, speed=0):
        try:
            return cls.objects.filter(content=chinese, type=cls.Type.WORD).get()
        except ObjectDoesNotExist:
            try:
                from aip import AipSpeech
                from jiezi_secret.secret import BAIDU_APP_ID, \
                    BAIDU_API_KEY, BAIDU_SECRET_KEY
            except (ModuleNotFoundError, ImportError):
                logger.warning("cannot connect to baidu API, use dummy instead")
                return cls.get_default()

            client = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
            request_kwargs = {
                'text': chinese,
                'lang': 'zh',
                'ctp': 1,
                'options': {'per': 5118, 'spd': speed, 'pit': 4, 'vol': 8},
            }
            result = client.synthesis(**request_kwargs)
            if not isinstance(result, dict):
                logger.info(f'successfully fetch {chinese} from baidu')
                audio_path = os.path.join(BASE_DIR, f'media/audio/{chinese}.mp3')
                audio_url = f'audio/{chinese}.mp3'
                with open(audio_path, 'wb') as f:
                    f.write(result)
                archive = json.dumps(request_kwargs, indent=4,
                                     ensure_ascii=False)
                return cls.objects.create(origin=cls.Origin.BAIDU,
                                          type=cls.Type.WORD,
                                          archive=archive,
                                          content=chinese,
                                          file=audio_url)
            else:
                logger.warning(f"fail Baidu API with {result}")
                return cls.get_default()

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
