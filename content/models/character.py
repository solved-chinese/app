from django.db import models
from django.core.exceptions import ValidationError
import json

from content.models import GeneralContentModel, OrderableMixin, \
    ReviewableMixin, AudioFile
from content.utils import validate_chinese_character_or_x
from content.data.makemeahanzi_dictionary import get_makemeahanzi_data


class DefinitionInCharacter(OrderableMixin):
    character = models.ForeignKey('Character', on_delete=models.CASCADE,
                             related_name='definitions',
                             related_query_name='definition')
    definition = models.CharField(max_length=70)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.definition

    def __repr__(self):
        return f"<Def of {self.character}: {str(self)}>"


class RadicalInCharacter(OrderableMixin):
    class RadicalType(models.TextChoices):
        __empty__ = 'TODO'
        SEMANTIC = 'semantic', 'semantic'
        PHONETIC = 'phonetic', 'phonetic'
        BOTH = 'both', 'both'
        NEITHER = 'neither', 'neither'

    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    radical = models.ForeignKey('Radical', on_delete=models.CASCADE)
    radical_type = models.CharField(choices=RadicalType.choices,
                                    max_length=12, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['character', 'radical', 'order']


class Character(ReviewableMixin, GeneralContentModel):
    class CharacterType(models.TextChoices):
        __empty__ = 'TODO'
        PICTOGRAPHIC = 'Pictographic', 'Pictographic'
        IDEOGRAPHIC = 'Ideographic', 'Ideographic'
        COMPOUND_IDEOGRAPHIC = 'Compound Ideographic', \
                               'Compound Ideographic'
        PICTO_PHONETIC = 'Picto-phonetic', 'Picto-phonetic'
        LOAN = 'Loan', 'Loan'

    chinese = models.CharField(max_length=1,
                               validators=[validate_chinese_character_or_x])
    identifier = models.CharField(max_length=10, blank=True)

    pinyin = models.CharField(max_length=40, default='TODO')
    audio = models.ForeignKey('AudioFile',
                              related_name='characters',
                              related_query_name='character',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)

    character_type = models.CharField(max_length=30,
                                      choices=CharacterType.choices,
                                      blank=True)
    radicals = models.ManyToManyField('Radical', related_name='characters',
                                      related_query_name='character',
                                      through='RadicalInCharacter')
    memory_aid = models.TextField(max_length=300,
                                  blank=True, default='TODO',
                                  verbose_name='character memory aid')

    class Meta:
        ordering = ['id']
        unique_together = ['chinese', 'identifier']

    def clean(self):
        super().clean()
        if self.is_done:
            if not self.radicals.exists():
                raise ValidationError('cannot be done without any radical')
            for r in self.radicals.all():
                if not r.is_done:
                    raise ValidationError(f"{repr(r)} not done")

            if not self.definitions.exists():
                raise ValidationError('cannot be done without any definition')
            for definition in self.definitions.all():
                if not definition.definition or 'TODO' in definition.definition:
                    raise ValidationError('definitions not done')

    def save(self, *args, **kwargs):
        adding = self._state.adding
        if not adding:
            old_self = Character.objects.get(pk=self.pk)
        # initial save is needed for foreign keys to be related to self
        super().save(*args, **kwargs)
        if adding:
            self.fill_data()
            # cannot also pass kwargs here or force_insert will produce an error
            super().save(check_chinese=False)
        if (adding or self.pinyin != old_self.pinyin) and \
                (not self.audio or self.audio.type != AudioFile.Type.CUSTOM):
            self.audio = AudioFile.get_by_pinyin(self.pinyin)
            super().save(check_chinese=False)

    def fill_data(self):
        """ this fills necessary data from makemeahanzi into archive field,
         remember to save """
        if self.chinese == 'x':
            return
        characters_data = get_makemeahanzi_data()
        try:
            data = characters_data[self.chinese]
        except KeyError:
            raise ValidationError(f"{self.chinese} is not proper character")

        if self.pinyin == 'TODO' or not self.pinyin:
            self.pinyin = data['pinyin']

        if not self.definitions.exists():
            definitions = data['definition'].split(';')
            for index, definition in enumerate(definitions):
                definition = definition.strip()
                DefinitionInCharacter.objects.create(
                    character=self, definition=definition, order=index
                )
            self.add_warning(f"definitions auto-generated, please verify")
        self.archive = json.dumps(data, indent=4, ensure_ascii=False)

    def reset_order(self):
        OrderableMixin.reset_order(self.radicalincharacter_set)
        OrderableMixin.reset_order(self.definitions)

    @property
    def audio_url(self):
        try:
            return self.audio.file.url
        except AttributeError:
            return AudioFile.get_default().url

    @property
    def full_definition(self):
        """ used in serializer """
        return "; ".join(map(str, self.definitions.all()))

    def __str__(self):
        if self.identifier:
            return f"{self.chinese}({self.identifier})"
        else:
            return self.chinese

    def __repr__(self):
        id = self.id or -1
        return f"<C{id:04d}:{self.chinese}#{self.identifier}>"

    @classmethod
    def get_TODO_character(cls):
        return cls.objects.get_or_create(
            chinese='x',
            defaults={'note': 'placeholder, do NOT edit this, '
                              'choose an actual character'}
        )[0]
