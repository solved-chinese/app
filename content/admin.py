from django.contrib import admin
from .models import Character, Radical, CharacterSet
from django.utils.html import format_html
from django.urls import reverse


class RadicalAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'id']
    list_display = ['__str__', 'get_characters_list_display']

    def get_characters_list_display(self, radical):
        s = ""
        for c in radical.characters.all():
            s += f"<a href={reverse('display_character', args=[c.pk])}>" \
                 f"{c.chinese}</a>, "
        return format_html(s)


admin.site.register(Radical, RadicalAdmin)


class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'id']
    list_display = ['__str__', 'id', 'radical_1', 'radical_2', 'radical_3']


admin.site.register(Character, CharacterAdmin)


class CharacterSetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'characters__chinese']
    filter_horizontal = ('characters', 'characters')


admin.site.register(CharacterSet, CharacterSetAdmin)
