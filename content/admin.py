from django.contrib import admin
from .models import Character, Radical, CharacterSet

admin.site.register(Radical)
admin.site.register(Character)
admin.site.register(CharacterSet)
