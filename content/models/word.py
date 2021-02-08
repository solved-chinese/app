from django.db import models
from django.core.exceptions import ValidationError
import re

from content.models import GeneralContentModel, OrderableMixin, \
    ReviewableMixin, AudioFile
from content.utils import validate_chinese_character_or_x


class DefinitionInWord(OrderableMixin):
    class PartOfSpeech(models.TextChoices):
        __empty__ = 'N/A'
        TODO = ' ', 'TODO'
        IDIOM = 'idiom', 'idiom'
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
                                      default=PartOfSpeech.TODO,
                                      blank=True)
    definition = models.CharField(max_length=200,
                                  blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        if self.part_of_speech not in ('', ' '):
            return f"{self.part_of_speech}. {self.definition}"
        else:
            return self.definition

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
    chinese_highlight = models.CharField(max_length=60)
    pinyin = models.CharField(max_length=200)
    pinyin_highlight = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    translation_highlight = models.CharField(max_length=200)
    audio = models.ForeignKey('AudioFile',
                              related_name='sentences',
                              related_query_name='sentence',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)

    def get_admin_url(self):
        return self.word.get_admin_url()

    @property
    def audio_url(self):
        try:
            return self.audio.file.url
        except AttributeError:
            return AudioFile.get_default().file.url

    @property
    def audio_speed(self):
        if self.word.IC_level is None:
            return 2
        elif self.word.IC_level < 10:
            return 1
        elif self.word.IC_level < 20:
            return 2
        else:
            return 3

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.chinese

    def __repr__(self):
        return f"<EgSent of {self.word}: {str(self)}>"


class Word(ReviewableMixin, GeneralContentModel):
    # TODO if word chinese field change, also change characters
    chinese = models.CharField(max_length=10)
    identifier = models.CharField(max_length=10, blank=True)

    pinyin = models.CharField(max_length=36, default='TODO')
    audio = models.ForeignKey('AudioFile',
                              related_name='words',
                              related_query_name='word',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)

    characters = models.ManyToManyField('Character',
                                        related_name='words',
                                        related_query_name='word',
                                        through='CharacterInWord')
    memory_aid = models.TextField(max_length=300,
                                  blank=True, default='TODO',
                                  verbose_name='word memory aid')

    class Meta:
        ordering = ['id']
        unique_together = ['chinese', 'identifier']

    def clean(self):
        """check that word and characters do not mismatch in chinese & pinyin"""
        super().clean()
        if self.is_done:
            if not self.characters.exists():
                raise ValidationError('cannot be done without any character')
            for c in self.characters.all():
                if not c.is_done:
                    raise ValidationError(f"{repr(c)} not done")

            if not self.definitions.exists():
                raise ValidationError('cannot be done with no definition')
            for index, definition in enumerate(self.definitions.all()):
                if not definition.definition:
                    raise ValidationError(f'definition {index + 1} empty')
                if definition.part_of_speech == \
                        DefinitionInWord.PartOfSpeech.TODO:
                    raise ValidationError(
                        f'definition {index + 1} part of speech not done')

            if not self.sentences.exists():
                raise ValidationError('cannot be done without any sentence')

    def save(self, *args, **kwargs):
        # if adding, connect the necessary characters
        if self._state.adding and self.chinese != 'x':
            # connect audio
            if len(self.chinese) == 1:
                self.audio = AudioFile.get_by_pinyin(self.pinyin)
            else:
                self.audio = AudioFile.get_by_chinese(self.audio_chinese)
            # connect related characters
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

    @property
    def audio_url(self):
        try:
            return self.audio.file.url
        except AttributeError:
            return AudioFile.get_default().file.url

    @property
    def audio_chinese(self):
        if '(' in self.chinese:
            return "{}, {}".format(
                re.sub(r"\(.*?\)", '', self.chinese),
                self.chinese.replace('(', '').replace(')', '')
            )
        return self.chinese

    @property
    def primary_definition(self):
        if self.definitions.exists():
            return str(self.definitions.first())
        return None

    @property
    def primary_sentence_chinese(self):
        if self.sentences.exists():
            return self.sentences.first().chinese
        return None

    @property
    def primary_sentence_pinyin(self):
        if self.sentences.exists():
            return self.sentences.first().pinyin
        return None

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
        return f"<W{id:04d}:{self.chinese}#{self.identifier}>"

    @classmethod
    def get_TODO_word(cls):
        return cls.objects.get_or_create(
            chinese='x',
            defaults={'note': 'placeholder, do NOT edit this, '
                              'choose an actual character'}
        )[0]
