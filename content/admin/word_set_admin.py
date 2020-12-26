from django.contrib import admin

from content.models import WordInSet, WordSet


class WordInSetInline(admin.TabularInline):
    model = WordInSet
    autocomplete_fields = ['word']
    readonly_fields = ['get_definitions']

    def get_definitions(self, wiws):
        w = wiws.word
        definitions = ""
        for d in w.definitions.all():
            definitions += f"{d.part_of_speech} {d.definition}; "
        return definitions


@admin.register(WordSet)
class WordSetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_done']
    list_filter = ['is_done']
    search_fields = ['name', 'characters__chinese']
    inlines = [WordInSetInline]
