from django import forms

from .models import WordSet, Word


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