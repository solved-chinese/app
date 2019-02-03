import os

from django.core.exceptions import ValidationError
from django.db import models
import accounts.models  # to avoid cyclic import
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, _path, _name):
        self.path = _path
        self.name = _name

    def __call__(self, instance, filename):
        if self.path == 'characters/':
            self.path += 'C%04d/' % instance.jiezi_id.to_internal_value
        elif self.path == 'radicals/':
            self.path += 'R%04d/' % instance.jiezi_id.to_internal_value
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(self.name, ext)
        return self.path + filename


character_pinyin_audio_path = PathAndRename('characters/', 'pinyin_audio')
character_color_coded_image_path = PathAndRename('characters/', 'color_coded_image')
character_stroke_order_image_path = PathAndRename('characters/', 'stroke_order_image')
radical_mnemonic_image_path = PathAndRename('radicals/', 'mnemonic_image')


# TODO delete the files after delete


class Radical(models.Model):
    jiezi_id = models.IntegerField(primary_key=True, help_text="enter integer only")
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=10, help_text="if it doesn't exist put --")
    definition = models.CharField(max_length=50)
    mnemonic_explanation = models.TextField(max_length=100)
    mnemonic_image = models.ImageField(upload_to=radical_mnemonic_image_path,
                                       default='default.jpg')  # TODO add height/width
    is_phonetic = models.BooleanField();
    is_semantic = models.BooleanField();

    class Meta:
        ordering = ['jiezi_id']

    def __str__(self):
        return 'R' + '%04d' % self.jiezi_id + ':' + self.chinese


class Character(models.Model):
    jiezi_id = models.IntegerField(primary_key=True, help_text="enter integer only")
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=10)
    definition_1 = models.CharField(max_length=50)
    definition_2 = models.CharField(max_length=50, null=True, blank=True)
    explanation_2 = models.CharField(max_length=200, null=True, blank=True)
    definition_3 = models.CharField(max_length=50, null=True, blank=True)
    explanation_3 = models.CharField(max_length=200, null=True, blank=True)

    pinyin_audio = models.FileField(upload_to=character_pinyin_audio_path, default='error.mp3', help_text='it is ok for now to leave blank')
    color_coded_image = models.ImageField(upload_to=character_color_coded_image_path,
                                          default='default.jpg')  # TODO add height/width
    stroke_order_image = models.ImageField(upload_to=character_stroke_order_image_path, default='default.jpg')

    mnemonic_explanation = models.TextField(max_length=200)
    mnemonic_1 = models.IntegerField(help_text="enter number only")
    mnemonic_2 = models.IntegerField(null=True, blank=True,
                                     help_text="enter number only, if it doens't exits, leave BLANK instead of putting 0")
    mnemonic_3 = models.IntegerField(null=True, blank=True,
                                     help_text="enter number only, if it doens't exits, leave BLANK instead of putting 0")

    example_1_word = models.CharField(max_length=5)
    example_1_pinin = models.CharField(max_length=25)
    example_1_character = models.CharField(max_length=50)
    example_1_meaning = models.CharField(max_length=50)
    example_2_word = models.CharField(max_length=5, null=True, blank=True)
    example_2_pinin = models.CharField(max_length=25, null=True, blank=True)
    example_2_character = models.CharField(max_length=50, null=True, blank=True)
    example_2_meaning = models.CharField(max_length=50, null=True, blank=True)

    def clean(self):
        print("clean called")
        if not Radical.objects.filter(pk=self.mnemonic_1).exists():
            raise ValidationError('mnemonic 1: R%04d not exist'%self.mnemonic_1, code='invalid')
        if self.mnemonic_2 is not None:
            if not Radical.objects.filter(pk=self.mnemonic_2).exists():
                raise ValidationError('mnemonic 2: R%04d not exist'%self.mnemonic_2, code='invalid')
            if self.mnemonic_3 is not None and not Radical.objects.filter(pk=self.mnemonic_3).exists():
                raise ValidationError('mnemonic 3: R%04d not exist'%self.mnemonic_3, code='invalid')
        elif self.mnemonic_3 is not None:
            raise ValidationError('mnemonic 2 is blank but mnemonic 3 is not, wtf!!!', code='invalid')

    def __str__(self):
        return 'C' + '%04d' % self.jiezi_id + ':' + self.chinese

    # a wrapper of __str__ as template doesn't allow for things starting with _ ...
    def to_string(self):
        return self.__str__()

    class Meta:
        ordering = ['jiezi_id']


class CharacterSet(models.Model):
    characters = models.ManyToManyField(Character)
    name = models.CharField(max_length=50)

    def add_to_user(self, user):
        if user.user_character_tags.filter(name=self.name).exists():
            raise accounts.models.UserCharacterTag.SameNameException
        tag = accounts.models.UserCharacterTag.objects.create(name=self.name, user=user)
        for character in self.characters.all():
            print(character.__str__())
            character_to_add = accounts.models.UserCharacter.objects.get_or_create(character=character, user=user)[0]
            tag.user_characters.add(character_to_add)

    def __str__(self):
        return self.name
