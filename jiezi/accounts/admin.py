from django.contrib import admin
from .models import User, UserCharacter, UserCharacterTag

admin.site.register(User)
admin.site.register(UserCharacter)
admin.site.register(UserCharacterTag)
