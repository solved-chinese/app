from django.contrib import admin

from learning.models import Character, CharacterSet, Radical, Report

admin.site.register(Radical)
admin.site.register(Character)
admin.site.register(CharacterSet)
admin.site.register(Report)