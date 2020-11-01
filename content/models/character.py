from django.core.exceptions import ValidationError
from django.db import models

from content.audio import get_audio
from content.models import DFModelMixin
from jiezi.utils.mixins import StrDefaultReprMixin, CleanBeforeSaveMixin


class Character(DFModelMixin, StrDefaultReprMixin, CleanBeforeSaveMixin,
                models.Model):
    TEST_FIELDS = ['pinyin', 'definition_1']

    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=15)
    part_of_speech_1 = models.CharField(max_length=50)
    definition_1 = models.CharField(max_length=100)
    part_of_speech_2 = models.CharField(max_length=50, null=True, blank=True)
    definition_2 = models.CharField(max_length=100, null=True, blank=True)
    part_of_speech_3 = models.CharField(max_length=50, null=True, blank=True)
    definition_3 = models.CharField(max_length=100, null=True, blank=True)

    radical_1 = models.ForeignKey('Radical', on_delete=models.CASCADE,
                                  related_name='+')
    radical_2 = models.ForeignKey('Radical', on_delete=models.CASCADE,
                                  related_name='+', null=True, blank=True)
    radical_3 = models.ForeignKey('Radical', on_delete=models.CASCADE,
                                  related_name='+', null=True, blank=True)
    mnemonic_explanation = models.CharField(max_length=800)

    example_1_word = models.CharField(max_length=10)
    example_1_pinyin = models.CharField(max_length=25)
    example_1_character = models.CharField(max_length=100)
    example_1_meaning = models.CharField(max_length=100)
    example_2_word = models.CharField(max_length=10, null=True, blank=True)
    example_2_pinyin = models.CharField(max_length=25, null=True, blank=True)
    example_2_character = models.CharField(max_length=100, null=True, blank=True)
    example_2_meaning = models.CharField(max_length=100, null=True, blank=True)

    is_preview_definition = models.BooleanField()
    is_preview_pinyin = models.BooleanField()
    structure = models.IntegerField(null=True)

    stroke_order_image = models.ImageField(default='default.jpg')

    def get_example_sentence(self, index=1):
        word = getattr(self, f'example_{index}_word')
        pinyin = getattr(self, f'example_{index}_pinyin')
        character = getattr(self, f'example_{index}_character')
        meaning = getattr(self, f'example_{index}_meaning')
        if not word and index == 2:
            return None

        assert len(word) == 2 or word.count('+') == 1,\
            f'example_{index}_word needs to be of length 2 or separated by a' \
            f'plus sign but "{word}" is not'
        if len(word) == 2:
            words = word
        else:
            words = word.split('+')


        assert pinyin.count(' ') == 1 or pinyin.count('+') == 1, \
            f'example_{index}_pinyin should contain 1 space or plus sign' \
            f'but "{pinyin} does not'
        if pinyin.count(' ') == 1:
            pinyin = pinyin.split(' ')
        else:
            pinyin = pinyin.split('+')

        assert character.count('+') == 1, f'example_{index}_pinyin should' \
            f' contain 1 "+" but "{character}" does not'
        characters = character.split('+')

        return f"&nbsp;&nbsp;&nbsp;" \
               f"{words[0]} /{pinyin[0].strip()}/ {characters[0].strip()}" \
               f" + {words[1]} /{pinyin[1].strip()}/ {characters[1].strip()}" \
               f"<br> = {word} {meaning}"

    def get_example_2_sentence(self):
        return self.get_example_sentence(index=2)

    @property
    def pinyin_audio(self):
        return get_audio(pinyin=self.pinyin)

    def clean(self):
        if self.radical_2 is None and self.radical_3 is not None:
            raise ValidationError('radical_2 is None but radical_3 exists')
        try:
            self.get_example_sentence()
        except AssertionError as e:
            raise ValidationError('example not valid') from e

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise Exception('self deletion') from e

    def __repr__(self):
        return '<C' + '%04d' % self.id + ':' + self.chinese +'>'

    class Meta:
        ordering = ['id']