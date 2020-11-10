from django.contrib import admin
from .models import Character, Radical, CharacterSet


class RadicalAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'id']


admin.site.register(Radical, RadicalAdmin)


class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['chinese', 'id']
    list_display = ['__str__', 'id', 'radical_1', 'radical_2', 'radical_3']


admin.site.register(Character, CharacterAdmin)


class CharacterSetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'characters__chinese']
    filter_horizontal = ('characters', 'characters')


admin.site.register(CharacterSet, CharacterSetAdmin)
