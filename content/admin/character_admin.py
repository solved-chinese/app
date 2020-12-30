from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import RadicalInCharacter, DefinitionInCharacter, Character


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
class CharacterAdmin(admin.ModelAdmin):
    readonly_fields = ['archive']
    search_fields = ['chinese', 'pinyin']
    list_display = ['__str__', 'is_done', 'get_word_list_display']
    list_filter = ['is_done', 'word__word_set__name']
    autocomplete_fields = ["radicals"]
    inlines = [DefinitionInCharacterInline, RadicalInCharacterInline]

    def get_word_list_display(self, character):
        s = ""
        for w in character.words.all().distinct():
            s += f"<a href={reverse('admin:content_word_change', args=[w.pk])}>" \
                 f"{w.chinese}</a>, "
        return format_html(s[:-2])

    get_word_list_display.short_description = "Used In"
