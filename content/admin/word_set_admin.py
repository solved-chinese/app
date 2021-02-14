from django.contrib import admin

from content.models import WordInSet, WordSet
from content.admin import GeneralContentAdmin


class WordInSetInline(admin.TabularInline):
    model = WordInSet
    autocomplete_fields = ['word']
    readonly_fields = ['is_done', 'get_definitions']
    extra = 0

    def is_done(self, obj):
        return '\u2705' if obj.word.is_done else '\u274c'

    def get_definitions(self, wiws):
        w = wiws.word
        definitions = ""
        for d in w.definitions.all():
            definitions += f"{d.part_of_speech} {d.definition}; "
        return definitions


@admin.register(WordSet)
class WordSetAdmin(GeneralContentAdmin):
    list_display = ['id', '__str__', 'render_all_words', 'is_done']
    list_filter = ['is_done']
    search_fields = ['name__search']
    inlines = [WordInSetInline]

