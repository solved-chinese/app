from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import TreeRelatedFieldListFilter

from content.models import CharacterInWord, DefinitionInWord, Sentence, Word
from content.admin import SpecificContentAdmin, ReviewableAdminMixin, \
    DisabledFieldMixin
from content.forms import SentenceForm, WordForm, WordCreationForm


class CharacterInWordInline(admin.TabularInline):
    model = CharacterInWord
    autocomplete_fields = ['character']
    readonly_fields = ['is_done', 'get_definitions']
    extra = 0

    def is_done(self, obj):
        return '\u2705' if obj.character.is_done else '\u274c'

    def get_definitions(self, ciw):
        c = ciw.character
        definitions = ""
        for definition in c.definitions.all():
            definitions += f"{definition.definition}; "
        return definitions


class DefinitionInWordInline(admin.TabularInline):
    model = DefinitionInWord
    extra = 0


class SentenceInline(DisabledFieldMixin, admin.StackedInline):
    model = Sentence
    extra = 0
    form = SentenceForm
    fieldsets = ((None, {
        'fields': (
            'order',
            ('audio', 'create_audio'),
            ('chinese', 'chinese_highlight'),
            ('pinyin', 'pinyin_highlight'),
            ('translation', 'translation_highlight'),
        ),
        'description': "Use <> to indicate highlight"
    }),)
    readonly_fields = ['chinese_highlight', 'pinyin_highlight',
                       'translation_highlight']
    autocomplete_fields = ['audio']
    disabled_fields = ['audio']


@admin.register(Word)
class WordAdmin(ReviewableAdminMixin, SpecificContentAdmin):
    search_fields = ['chinese', 'pinyin', 'identifier']
    list_display = ['id', 'is_done', '__str__', 'pinyin',
                    'get_definitions', 'get_set_list_display']
    list_filter = [('is_done', admin.BooleanFieldListFilter),
                   ('word_set', TreeRelatedFieldListFilter),
                   ('IC_level', admin.EmptyFieldListFilter),]
    readonly_fields = ('get_set_list_display',)
    autocomplete_fields = ('audio',)
    inlines = [DefinitionInWordInline, SentenceInline, CharacterInWordInline]
    form = WordForm

    def get_form(self, request, obj=None, **kwargs):
        """
        User a special from for creation
        reference django.contrib.auth.admin.UserAdmin.get_form
        """
        defaults = {}
        if obj is None:
            defaults['form'] = WordCreationForm
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_disabled_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.disabled_fields
        else:
            return super().get_disabled_fields(request, obj=obj)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'definitions', 'word_sets')

    def get_definitions(self, word):
        s = ""
        for definition in word.definitions.all():
            s += f"{definition} <br>"
        return format_html(s)
    get_definitions.short_description = "definitions"

    def get_set_list_display(self, word):
        s = ""
        for ws in word.word_sets.all().distinct():
            s += f"<a href={reverse('admin:content_wordset_change', args=[ws.pk])}>" \
                 f"{ws.name}</a>, "
        return format_html(s[:-2])
    get_set_list_display.short_description = "Used In"
