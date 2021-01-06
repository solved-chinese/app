from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import RadicalInCharacter, DefinitionInCharacter, Character
from content.admin import GeneralContentAdmin, MultiSelectFieldListFilter


class RadicalInCharacterInline(admin.TabularInline):
    model = RadicalInCharacter
    autocomplete_fields = ['radical']
    readonly_fields = ['radical_definition', 'radical_pinyin']
    extra = 0

    def radical_definition(self, obj):
        return obj.radical.definition

    def radical_pinyin(self, obj):
        return obj.radical.pinyin


class DefinitionInCharacterInline(admin.TabularInline):
    model = DefinitionInCharacter
    extra = 0


@admin.register(Character)
class CharacterAdmin(GeneralContentAdmin):
    search_fields = ['chinese', 'pinyin', 'identifier']
    list_display = ['id', 'is_done', '__str__', 'pinyin',
                    'get_definitions', 'get_word_list_display']
    list_filter = [('is_done', admin.BooleanFieldListFilter),
                   ('word__word_set__name', MultiSelectFieldListFilter)]
    autocomplete_fields = ["radicals"]
    inlines = [DefinitionInCharacterInline, RadicalInCharacterInline]

    def get_definitions(self, character):
        s = ""
        for definition in character.definitions.all():
            s += f"{definition} <br>"
        return format_html(s)
    get_definitions.short_description = "definitions"

    def get_word_list_display(self, character):
        s = ""
        for w in character.words.all().distinct():
            s += f"<a href={reverse('admin:content_word_change', args=[w.pk])}>" \
                 f"{w.chinese}</a>, "
        return format_html(s[:-2])

    get_word_list_display.short_description = "Used In"
