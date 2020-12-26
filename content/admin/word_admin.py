from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import CharacterInWord, DefinitionInWord, Sentence, Word


class CharacterInWordInline(admin.TabularInline):
    model = CharacterInWord
    autocomplete_fields = ['character']
    readonly_fields = ['get_definitions']
    extra = 0

    def get_definitions(self, ciw):
        c = ciw.character
        definitions = ""
        for definition in c.definitions.all():
            definitions += f"{definition.definition}; "
        return definitions


class DefinitionInWordInline(admin.TabularInline):
    model = DefinitionInWord
    extra = 0


class SentenceInline(admin.TabularInline):
    model = Sentence
    extra = 0


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'pinyin']
    list_display = ['__str__', 'is_done', 'get_set_list_display']
    list_filter = ['is_done']
    inlines = [CharacterInWordInline, DefinitionInWordInline,
               SentenceInline]

    def get_set_list_display(self, word):
        s = ""
        for ws in word.word_sets.all().distinct():
            s += f"<a href={reverse('admin:content_wordset_change', args=[ws.pk])}>" \
                 f"{ws.name}</a>, "
        return format_html(s[:-2])
    get_set_list_display.short_description = "Used In"
