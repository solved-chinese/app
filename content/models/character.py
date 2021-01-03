from django.db import models
from django.core.exceptions import ValidationError
import json

from content.models import GeneralContentModel, OrderableMixin, \
    validate_chinese_character_or_x
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


class Character(GeneralContentModel):
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
    character_type = models.CharField(max_length=30,
                                      choices=CharacterType.choices,
                                      blank=True)
    radicals = models.ManyToManyField('Radical', related_name='characters',
                                      related_query_name='character',
                                      through='RadicalInCharacter')
    memory_aid = models.TextField(max_length=300,
                                  blank=True, default='TODO',
                                  verbose_name='word memory aid')

    class Meta:
        unique_together = ['chinese', 'identifier']

    def get_child_models(self):
        radicals = list(self.radicals.all())
        return [(repr(radical), radical) for radical in radicals]

    def clean(self):
        super().clean()
        if self.is_done:
            if not self.radicals.exists():
                raise ValidationError('cannot be done without any radical')
            if not self.definitions.exists():
                raise ValidationError('cannot be done without any definition')
            for definition in self.definitions.all():
                if not definition.definition or 'TODO' in definition.definition:
                    raise ValidationError('definitions not done')

    def save(self, *args, **kwargs):
        adding = self._state.adding
        # initial save is needed for foreign keys to be related to self
        super().save(*args, **kwargs)
        if adding:
            self.fill_makemeahanzi_data()
            super().save(*args, check_chinese=False, **kwargs)

    def fill_makemeahanzi_data(self):
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

    def __str__(self):
        if self.identifier:
            return f"{self.chinese}({self.identifier})"
        else:
            return self.chinese

    def __repr__(self):
        return f"<C{self.id:04d}:{self.chinese}#{self.identifier}>"

    def get_absolute_url(self):
        return f"/learning/display/?t=character&qid={self.pk}"

    @classmethod
    def get_TODO_character(cls):
        return cls.objects.get_or_create(
            chinese='x',
            defaults={'note': 'placeholder, do NOT edit this, '
                              'choose an actual character'}
        )[0]
