from django.contrib import admin

from content.models import WordInSet, WordSet
from content.forms import WordSetQuickCreateFrom
from content.admin import GeneralContentAdmin


class WordInSetInline(admin.TabularInline):
    model = WordInSet
    autocomplete_fields = ['word']
    readonly_fields = ['get_definitions']
    extra = 0

    def get_definitions(self, wiws):
        w = wiws.word
        definitions = ""
        for d in w.definitions.all():
            definitions += f"{d.part_of_speech} {d.definition}; "
        return definitions


@admin.register(WordSet)
class WordSetAdmin(GeneralContentAdmin):
    list_display = ['id', '__str__', 'is_done']
    list_filter = ['is_done']
    search_fields = ['name', 'characters__chinese']
    inlines = [WordInSetInline]

    def get_form(self, request, obj=None, **kwargs):
        """
        User a special from for creation
        reference django.contrib.auth.admin.UserAdmin.get_form
        """
        defaults = {}
        if obj is None:
            defaults['form'] = WordSetQuickCreateFrom
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
