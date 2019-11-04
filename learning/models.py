import pandas as pd
import numpy as np

from django.db import models
import accounts.models  # to avoid cyclic import


class Radical(models.Model):
    id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=15)
    definition = models.CharField(max_length=100)
    mnemonic_explanation = models.CharField(max_length=300, null=True, blank=True)
    mnemonic_image = models.ImageField(default='default.jpg')
    is_phonetic = models.BooleanField()
    is_semantic = models.BooleanField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '<R' + '%04d' % self.id + ':' + self.chinese +'>'


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=15)
    part_of_speech_1 = models.CharField(max_length=50)
    definition_1 = models.CharField(max_length=100)
    part_of_speech_2 = models.CharField(max_length=50, null=True, blank=True)
    definition_2 = models.CharField(max_length=100, null=True, blank=True)
    explanation_2 = models.CharField(max_length=300, null=True, blank=True)
    part_of_speech_3 = models.CharField(max_length=50, null=True, blank=True)
    definition_3 = models.CharField(max_length=100, null=True, blank=True)
    explanation_3 = models.CharField(max_length=300, null=True, blank=True)

    radical_1_id = models.IntegerField()
    radical_2_id = models.IntegerField(null=True, blank=True)
    radical_3_id = models.IntegerField(null=True, blank=True)
    mnemonic_explanation = models.CharField(max_length=400)

    example_1_word = models.CharField(max_length=5)
    example_1_pinyin = models.CharField(max_length=25)
    example_1_character = models.CharField(max_length=50)
    example_1_meaning = models.CharField(max_length=50)
    example_2_word = models.CharField(max_length=5, null=True, blank=True)
    example_2_pinyin = models.CharField(max_length=25, null=True, blank=True)
    example_2_character = models.CharField(max_length=50, null=True, blank=True)
    example_2_meaning = models.CharField(max_length=50, null=True, blank=True)

    is_preview_definition = models.BooleanField()
    is_preview_pinyin = models.BooleanField()
    structure = models.IntegerField(null=True)

    color_coded_image = models.ImageField(default='default.jpg')
    stroke_order_image = models.ImageField(default='default.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Radical.objects.filter(pk=self.radical_1_id).exists() or \
                self.radical_2_id and not Radical.objects.filter(pk=self.radical_2_id).exists() or \
                self.radical_3_id and not Radical.objects.filter(pk=self.radical_3_id).exists():
            self.delete()
            raise Exception('related radicals not exist, self deletion')

    def __str__(self):
        return '<C' + '%04d' % self.id + ':' + self.chinese +'>'

    class Meta:
        ordering = ['id']


class CharacterSet(models.Model):
    characters = models.ManyToManyField(Character)
    name = models.CharField(max_length=50)

    def add_to_user(self, user):
        if user.user_character_tags.filter(name=self.name).exists():
            raise Exception('ERROR: a set with the same name already exists')
        tag = accounts.models.UserCharacterTag.objects.create(name=self.name, user=user)
        for character in self.characters.all():
            character_to_add = accounts.models.UserCharacter.objects.get_or_create(
                character=character, user=user)[0]
            tag.user_characters.add(character_to_add)

    def __str__(self):
        return f'<cset{self.id}:{self.name}>'


class Report(models.Model):
    user = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL)
    origin = models.CharField(max_length=100)
    description_1 = models.CharField(max_length=100)
    description_2 = models.TextField()

    def __str__(self):
        return f'<Report on {self.origin}: {self.description_1}>'

    class Meta:
        ordering = ['origin']


def update_from_df(df, Model):
    df.replace('', None, inplace=True)
    df.fillna(0, inplace=True)
    messages = []
    good_pk = []
    for i, row in df.iterrows():
        try:
            id = row['id']
            if id == 0:
                messages.append(f'ERR at start : row {i} id not found')
                continue
            if '√' not in str(row['Comments']):
                if Model.objects.filter(pk=id).exists():
                    messages.append(f'WARNING: delete id={id}')
                continue
            data = {}
            for field in Model._meta.get_fields():
                if field.name == 'id':
                    continue
                if isinstance(field, (models.IntegerField, models.BooleanField)):
                    data[field.name]=row[field.name]
                elif isinstance(field, models.CharField):
                    # FIXME per request of LING team, remove all stars from str
                    data[field.name] = row[field.name].replace('*', '') \
                        if row[field.name] else None
        except Exception as e:
            messages.append(f'ERR getting fields of id={id}: {str(e)}')
            continue
        try:
            _, is_created = Model.objects.update_or_create(id=id, defaults=data)
            messages.append(f"{'create' if is_created else 'update'} id={id}")
            good_pk.append(id)
        except Exception as e:
            messages.append(f'ERR constructing id={id}: {str(e)}')

    Model.objects.exclude(pk__in=good_pk).delete()
    # TODO possibly add delete warning

    for i, msg in enumerate(messages, 0):
        if msg[0]=='E':
            messages[i] = '<div style="color:red;">' + msg + '</div>'
        elif msg[0]=='W':
            messages[i] = '<div style="color:orange;">' + msg + '</div>'
        else: messages[i] = '<div style="color:green;">' + msg + '</div>'
    return messages
