from django import forms
from dal_select2.widgets import Select2WidgetMixin
from dal.widgets import WidgetMixin

from .models import WordSet, Word, Sentence, LinkedField, AudioFile


class WordSetQuickCreateFrom(forms.ModelForm):
    words = forms.CharField(
        widget=forms.Textarea,
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
        fields = ['name', 'words']


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

    def save(self, commit=True):
        self.instance.add_highlight()
        if self.cleaned_data.get('create_audio', False):
            self.instance.audio = AudioFile.get_by_chinese(
                self.instance.chinese, speed=self.instance.audio_speed)
        return super().save(commit=commit)
