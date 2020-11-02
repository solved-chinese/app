from django.core.exceptions import ValidationError
from django.db import models

from content.audio import get_audio
from content.models import DFModelMixin
from jiezi.utils.mixins import CleanBeforeSaveMixin


class Character(DFModelMixin, CleanBeforeSaveMixin, models.Model):
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

        if '+' in word:
            words = word.split('+')
        else:
            words = word
        word_len = len(words)

        assert pinyin.count(' ') == 1 or pinyin.count('+') == 1, \
            f'example_{index}_pinyin should contain 1 space or plus sign' \
            f'but "{pinyin} does not'
        if pinyin.count(' ') == 1:
            pinyins = pinyin.split(' ')
        else:
            pinyins = pinyin.split(' ')
        pinyin_len = len(pinyins)

        characters = character.split('+')
        character_len = len(characters)

        assert character_len == pinyin_len == word_len,\
            f"character_len={character_len} word_len={word_len} " \
            f"pinyin_len={pinyin_len} need to be equal"
        assert character_len > 1, 'the length needs to be greater than 1'

        example = "&nbsp;&nbsp;&nbsp;"
        for i in range(character_len):
            example += f"{words[i]} /{pinyins[i]}/ {characters[i]}"
            if i != character_len - 1:
                example += ' + '
        example += f"<br> = {word.replace('+', '')} {meaning}"
        return example

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
            raise ValidationError(f'example not valid: {str(e)}') from e

    def __str__(self):
        return self.chinese

    def __repr__(self):
        return '<C' + '%04d' % self.id + ':' + self.chinese +'>'

    class Meta:
        ordering = ['id']
