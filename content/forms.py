import re
from django import forms
from dal_select2.widgets import Select2WidgetMixin
from dal.widgets import WidgetMixin
from django.core.exceptions import ValidationError

from .models import WordSet, Word, Character, LinkedField, AudioFile, \
    CharacterInWord
from .utils import punctuate_English, punctuate_Chinese, add_highlight, unaccent
from content.utils import validate_chinese_character_or_x


class WordSetCreationForm(forms.ModelForm):
    words = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="input each word in a new line"
    )

    def clean_words(self):
        words = self.cleaned_data['words']
        words = words.split('\n')
        cleaned_words = []
        for word in words:
            word = word.strip()
            if not word:
                continue
            word_objects = Word.objects.filter(chinese=word)
            cnt = word_objects.count()
            if cnt == 1:
                word_object = word_objects.get()
            elif cnt > 1:
                word_object = Word.get_TODO_word()
            else:
                word_object = Word.objects.get_or_create(
                    chinese=word)[0]
            cleaned_words.append(word_object)
        return cleaned_words

    class Meta:
        model = WordSet
        fields = ['name', 'jiezi_id', 'parent', 'words']


class LinkedFieldModelSelect2(WidgetMixin,
                              Select2WidgetMixin,
                              forms.Select):
    def filter_choices_to_render(self, selected_choices):
        """render the current choice as number only"""
        if selected_choices:
            assert len(selected_choices) == 1
            selected_choice = selected_choices[0]
            self.choices = [(selected_choice, selected_choice)]


class LinkedFieldForm(forms.ModelForm):
    object_id = forms.IntegerField(
        widget=LinkedFieldModelSelect2(
            url='linked_field_autocomplete',
            forward=('content_type', 'field_name')
        ), required=False
    )

    class Meta:
        model = LinkedField
        fields = ['overwrite', 'content_type', 'object_id', 'field_name']


class SentenceForm(forms.ModelForm):
    create_audio = forms.BooleanField(required=False)

    def add_highlight(self):
        instance = self.instance
        if 'chinese' in self.changed_data:
            instance.chinese = punctuate_Chinese(instance.chinese)
            instance.chinese, instance.chinese_highlight = \
                add_highlight(instance.chinese, instance.word.chinese,
                              mode='Chinese')
        if 'pinyin' in self.changed_data:
            instance.pinyin = punctuate_English(instance.pinyin)
            instance.pinyin, instance.pinyin_highlight = \
                add_highlight(instance.pinyin, instance.word.pinyin,
                              mode='English')
        if 'translation' in self.changed_data:
            instance.translation = punctuate_English(instance.translation)
            instance.translation, instance.translation_highlight = \
                add_highlight(
                    instance.translation,
                    *list(instance.word.definitions.values_list(
                            'definition', flat=True)),
                    mode='English'
                )

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.add_highlight()
        if self.cleaned_data.get('create_audio', False):
            self.instance.audio = AudioFile.get_by_chinese(
                self.instance.chinese, speed=self.instance.audio_speed)
        return super().save(commit=commit)


class ContentCreationForm(forms.ModelForm):
    class Meta:
        fields = ('chinese', 'identifier')


class WordSetSplitForm(forms.ModelForm):
    def __init__(self, *args, old_wordset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_wordset = old_wordset
        self.fields['words'] = forms.ModelMultipleChoiceField(
            queryset=old_wordset.words.all(),
            widget=forms.CheckboxSelectMultiple
        )

    def save(self, commit=True):
        assert commit
        self.instance.parent = self.old_wordset
        super().save(commit=True)
        self.old_wordset.words.remove(*self.instance.words.all())
        return self.instance

    class Meta:
        model = WordSet
        fields = ('name', 'jiezi_id', 'words')


class SearchablePinyinFormMixin:
    def save(self, commit=True):
        if ('pinyin' in self.changed_data
                and self.instance.pinyin
                and 'TODO' not in self.instance.pinyin):
            self.instance.searchable_pinyin = re.sub(
                r'[\ \(\)\-\,\'\.\/]', r'', unaccent(self.instance.pinyin).lower())
        return super().save(commit=commit)

    class Meta:
        help_texts = {
            'searchable_pinyin': 'To search this object, users need to enter '
                                 'exactly this string (case insensitive). This '
                                 'is auto-generated from pinyin. If there is a'
                                 ' need for change, contact chenyx.'
        }


class WordForm(SearchablePinyinFormMixin, forms.ModelForm):
    def save(self, commit=True):
        # assert commit, 'no commit not supported'
        instance = super().save(commit=False)
        if 'chinese' in self.changed_data:
            # connect audio
            if len(instance.chinese) == 1:
                instance.audio = AudioFile.get_by_pinyin(instance.pinyin)
            else:
                instance.audio = AudioFile.get_by_chinese(instance.audio_chinese)
            # connect related characters, only when creating
            if instance.pk is not None:
                instance.add_warning('Modifying chinese after creation, please '
                                     'manually change characters')
            else:
                character_objects = []
                for index, chinese in enumerate(instance.chinese):
                    try:
                        validate_chinese_character_or_x(chinese)
                    except ValidationError:
                        instance.add_warning(f"non-chinese characters '{chinese}' at "
                                             f"index {index}, please verify")
                        continue
                    characters = Character.objects.filter(chinese=chinese)
                    cnt = characters.count()
                    if cnt == 1:
                        character = characters.get()
                    elif cnt > 1:
                        instance.add_warning(
                            f"{chinese} at index {index} have more than one "
                            f"characters, please select manually")
                        character = Character.get_TODO_character()
                    else:
                        character = Character.objects.create(chinese=chinese)
                    character_objects.append(character)

                def _save_m2m():
                    for index, character in enumerate(character_objects):
                        CharacterInWord.objects.create(
                            character=character, word=instance, order=index)
                self._save_m2m = _save_m2m

        return super().save(commit=commit)


class CharacterForm(SearchablePinyinFormMixin, forms.ModelForm):
    pass


class RadicalForm(SearchablePinyinFormMixin, forms.ModelForm):
    pass


class WordCreationForm(ContentCreationForm, WordForm):
    pass
