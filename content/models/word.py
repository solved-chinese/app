from django.db import models
from django.core.exceptions import ValidationError
import unicodedata

from content.models import GeneralContentModel, OrderableMixin, \
    validate_chinese_character_or_x


class DefinitionInWord(OrderableMixin):
    class PartOfSpeech(models.TextChoices):
        __empty__ = 'TODO'
        ADJ = 'adj', 'adjective'
        ADV = 'adv', 'adverb'
        CONJ = 'conj', 'conjunction'
        INTERJ = 'interj', 'interjection'
        M = 'm', 'measure word'
        MV = 'mv', 'modal verb'
        N = 'n', 'noun'
        NU = 'nu', 'numeral'
        P = 'p', 'particle'
        PN = 'pn', 'proper noun'
        PR = 'pr', 'pronoun'
        PREFIX = 'prefix', 'prefix'
        PREP = 'prep', 'preposition'
        QP = 'qp', 'question particle'
        QPR = 'qpr', 'question pronoun'
        T = 't', 'time word'
        V = 'v', 'verb'
        VC = 'vc', 'verb plus complement'
        VO = 'vo', 'verb plus object'

    word = models.ForeignKey('Word', on_delete=models.CASCADE,
                             related_name='definitions',
                             related_query_name='definition')
    part_of_speech = models.CharField(max_length=6,
                                      choices=PartOfSpeech.choices,
                                      blank=True)
    definition = models.CharField(max_length=200,
                                  blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.part_of_speech}. {self.definition}"

    def __repr__(self):
        return f"<Def of {self.word}: {str(self)}>"


class CharacterInWord(OrderableMixin):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['character', 'word', 'order']


class Sentence(OrderableMixin):
    word = models.ForeignKey('Word', on_delete=models.CASCADE,
                             related_name='sentences',
                             related_query_name='sentence')
    chinese = models.CharField(max_length=40)
    pinyin = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.chinese

    def __repr__(self):
        return f"<EgSent of {self.word}: {str(self)}>"


class Word(GeneralContentModel):
    # TODO if word chinese field change, also change characters
    chinese = models.CharField(max_length=10)
    identifier = models.CharField(max_length=10, blank=True)

    pinyin = models.CharField(max_length=36, default='TODO')

    characters = models.ManyToManyField('Character',
                                        related_name='words',
                                        related_query_name='word',
                                        through='CharacterInWord')
    memory_aid = models.TextField(max_length=300,
                                  blank=True, default='TODO',
                                  verbose_name='word memory aid')

    class Meta:
        unique_together = ['chinese', 'identifier']

    def clean(self):
        """check that word and characters do not mismatch in chinese & pinyin"""
        super().clean()
        if self.is_done:
            if not self.characters.exists():
                raise ValidationError('cannot be done without any character')

            if not self.sentences.exists():
                raise ValidationError('cannot be done without any sentence')

    def get_child_models(self):
        characters = list(self.characters.all())
        return [(repr(c), c) for c in characters]

    def save(self, *args, **kwargs):
        adding = self._state.adding
        # if adding, connect the necessary characters
        if adding and self.chinese != 'x':
            from content.models import Character
            character_objects = []
            for index, chinese in enumerate(self.chinese):
                try:
                    validate_chinese_character_or_x(chinese)
                except ValidationError:
                    self.add_warning(f"non-chinese characters '{chinese}' at "
                                     f"index {index}, please verify")
                    continue
                characters = Character.objects.filter(chinese=chinese)
                cnt = characters.count()
                if cnt == 1:
                    character = characters.get()
                elif cnt > 1:
                    self.add_warning(f"{chinese} at index {index} have more than"
                        f" one characters, please select manually")
                    character = Character.get_TODO_character()
                else:
                    character = Character.objects.create(chinese=chinese)
                character_objects.append(character)
            super().save(*args, **kwargs)
            for index, character in enumerate(character_objects):
                CharacterInWord.objects.create(character=character,
                                               word=self, order=index)
        else:
            super().save(*args, **kwargs)

    def reset_order(self):
        OrderableMixin.reset_order(self.characterinword_set)
        OrderableMixin.reset_order(self.sentences)
        OrderableMixin.reset_order(self.definitions)

    def __str__(self):
        if self.identifier:
            return f"{self.chinese}({self.identifier})"
        else:
            return self.chinese

    def __repr__(self):
        return f"<W{self.id:04d}:{self.chinese}#{self.identifier}>"

    @classmethod
    def get_TODO_word(cls):
        return cls.objects.get_or_create(
            chinese='x',
            defaults={'note': 'placeholder, do NOT edit this, '
                              'choose an actual character'}
        )[0]
