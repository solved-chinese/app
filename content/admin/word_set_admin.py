from django.contrib import admin
from django.shortcuts import redirect, reverse
from mptt.admin import DraggableMPTTAdmin

from content.models import WordInSet, WordSet
from content.admin import GeneralContentAdmin
from content.forms import WordSetCreationForm


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
class WordSetAdmin(DraggableMPTTAdmin, GeneralContentAdmin):
    list_display = ['tree_actions', 'indented_title', 'jiezi_id', 'is_done']
    list_editable = ['jiezi_id', 'is_done']
    list_display_links = ('indented_title',)
    list_filter = ['is_done']
    search_fields = ['name__search']
    actions = ['split_wordset']
    inlines = [WordInSetInline]
    mptt_level_indent = 30

    def get_form(self, request, obj=None, **kwargs):
        """
        User a special from for creation
        reference django.contrib.auth.admin.UserAdmin.get_form
        """
        defaults = {}
        if obj is None:
            defaults['form'] = WordSetCreationForm
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def split_wordset(self, request, queryset):
        qs_cnt = queryset.count()
        if qs_cnt != 1:
            self.message_user(request,
                              f"error: can select only 1 but {qs_cnt} received")
            return
        return redirect(reverse('split_wordset', args=(queryset.get().pk,)))

    def rebuild(self, request, queryset):
        WordSet.objects.rebuild()
