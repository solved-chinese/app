from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import RadicalInCharacter, DefinitionInCharacter, Character


class RadicalInCharacterInline(admin.TabularInline):
    model = RadicalInCharacter
    autocomplete_fields = ['radical']
    extra = 0


class DefinitionInCharacterInline(admin.TabularInline):
    model = DefinitionInCharacter
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    readonly_fields = ['archive']
    search_fields = ['chinese', 'pinyin']
    list_display = ['__str__', 'is_done', 'get_word_list_display']
    list_filter = ['is_done']
    autocomplete_fields = ["radicals"]
    inlines = [RadicalInCharacterInline, DefinitionInCharacterInline]

    def get_word_list_display(self, character):
        s = ""
        for w in character.words.all().distinct():
            s += f"<a href={reverse('admin:content_word_change', args=[w.pk])}>" \
                 f"{w.chinese}</a>, "
        return format_html(s[:-2])

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    get_word_list_display.short_description = "Used In"
