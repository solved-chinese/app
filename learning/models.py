import pandas as pd
import numpy as np
import html
from django.core.exceptions import ValidationError

from django.db import models
import accounts.models  # to avoid cyclic import


class DFModel(models.Model):
    """
    This is the base for all models that rely on dataframe to update its
    objects.
    Fields are pulled from spreadsheet as such:
    if field blank, set value to None
    if Integer/Boolean/String, direct conversion
    if ForeignField/OneToOneFIeld, find using pk
    if ManyToManyField, add the pks of all columns with the same field name

    At the same time, this class calls full_clean() before saving
    """
    id = models.IntegerField(primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return repr(self)

    @classmethod
    def update_from_df(cls, df):
        """
        This function pulls the models from the given dataframe.
        Every row of the Dataframe object must represent a object, with a
        mandatory field id.
        :param df: A Dataframe object
        :param validate: this can  be overridden validate(row) must returns a
         tuple (is_ok, msg), is_ok is a boolean saying whether this row is
         valid, and msg is a str telling what is wrong if it is not valid
        :return: a dict (id: msg) where msg is a HTML div ready for display
        """
        df.replace('', None, inplace=True)
        df.fillna(0, inplace=True)
        messages = []
        good_pk = []
        m2m_fields = []
        warning = ""
        for i, row in df.iterrows():
            try:
                id = row['id']
                if id == 0:
                    messages.append(f'ERR at start : row {i} id not found')
                    continue
                # TODO make this a special validator
                if '√' not in str(row['Comments']):
                    if cls.objects.filter(pk=id).exists():
                        messages.append(f'WARNING: delete id={id} due to no '
                                        f'check in comment')
                    else:
                        messages.append(f'IGNORE: ignore id={id} due to no '
                                        f'check in comment')
                    continue
                data = {}
                for field in cls._meta.get_fields():
                    if field.name == 'id':
                        continue
                    if isinstance(field,
                                  (models.IntegerField, models.BooleanField)):
                        data[field.name] = row[field.name]
                    elif isinstance(field, models.CharField):
                        # FIXME per request of LING team, remove all stars from str
                        data[field.name] = row[field.name].strip().replace('*', '') \
                            if row[field.name] else None
                    elif isinstance(field, (models.OneToOneField,
                                            models.ForeignKey)):
                        data[field.name] = \
                            field.related_model.objects.get(pk=row[field.name]) \
                                if row[field.name] else None
                    elif isinstance(field, models.ManyToManyField):
                        m2m_fields.append(field)

            except Exception as e:
                try:
                    field
                except NameError:
                    field = None
                messages.append(
                    f'ERR getting field {field} of id={id}: {repr(e)}')
                continue

            try:
                obj, is_created = cls.objects.update_or_create(id=id,
                                                               defaults=data)
                row = row.groupby(level=0).agg(list).to_dict()
                for field in m2m_fields:
                    pks = row[field.name]
                    related_objs = []
                    for pk in pks:
                        pk = int(pk)
                        if not pk:
                            continue
                        try:
                            related_obj = field.related_model.objects.get(pk=pk)
                            related_objs.append(related_obj)
                        except field.related_model.DoesNotExist:
                            warning += f'\n{field} has no related object ' \
                                       f'with id={pk}'
                    getattr(obj, field.name).set(related_objs)
                if warning:
                    warning = f'WARNING though completed: {warning}\n'
                messages.append(f"{warning}"
                                f"{'create' if is_created else 'update'} {obj}")
                good_pk.append(id)
            except Exception as e:
                messages.append(f'ERR constructing id={id}: {repr(e)}')

        cls.objects.exclude(pk__in=good_pk).delete()
        # TODO possibly add delete warning

        for i, msg in enumerate(messages, 0):
            msg = f'<pre>{html.escape(msg)}</pre>'
            if msg[5] == 'E':
                messages[i] = '<div style="color:red;">' + msg + '</div>'
            elif msg[5] == 'W':
                messages[i] = '<div style="color:orange;">' + msg + '</div>'
            elif msg[5] == "I":
                messages[i] = '<div style="color:gray;">' + msg + '</div>'
            else:
                messages[i] = '<div style="color:green;">' + msg + '</div>'
        return messages

    class Meta:
        abstract = True

class Radical(DFModel):
    chinese = models.CharField(max_length=6)
    pinyin = models.CharField(max_length=15)
    definition = models.CharField(max_length=100)
    mnemonic_explanation = models.CharField(max_length=300, null=True, blank=True)
    mnemonic_image = models.ImageField(default='default.jpg')
    is_phonetic = models.BooleanField()
    is_semantic = models.BooleanField()

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return '<R' + '%04d' % self.id + ':' + self.chinese +'>'


class Character(DFModel):
    TEST_FIELDS = ['pinyin', 'definition_1']
    chinese = models.CharField(max_length=1)
    pinyin = models.CharField(max_length=15)
    part_of_speech_1 = models.CharField(max_length=50)
    definition_1 = models.CharField(max_length=100)
    part_of_speech_2 = models.CharField(max_length=50, null=True, blank=True)
    definition_2 = models.CharField(max_length=100, null=True, blank=True)
    part_of_speech_3 = models.CharField(max_length=50, null=True, blank=True)
    definition_3 = models.CharField(max_length=100, null=True, blank=True)

    radical_1 = models.ForeignKey(Radical, on_delete=models.CASCADE,
                                  related_name='+')
    radical_2 = models.ForeignKey(Radical, on_delete=models.CASCADE,
                                  related_name='+', null=True, blank=True)
    radical_3 = models.ForeignKey(Radical, on_delete=models.CASCADE,
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


        assert pinyin.count(' ') == 1 or pinyin.count('+'), \
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


class CharacterSet(DFModel):
    characters = models.ManyToManyField(Character)
    name = models.CharField(max_length=50)

    def __repr__(self):
        return f'<cset{self.id}:{self.name} ' \
               f'{[repr(c) for c in self.characters.all()]}>'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for uctag in self.user_character_tags.all():
            uctag.update_from_character_set() # FIXME make more efficient


class Report(models.Model):
    user = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL)
    origin = models.CharField(max_length=100)
    description_1 = models.CharField(max_length=100)
    description_2 = models.TextField()

    def __repr__(self):
        return f'<Report on {self.origin}: {self.description_1}>'

    def __str__(self):
        return repr(self)

    class Meta:
        ordering = ['origin']
