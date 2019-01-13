from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserCharacter, UserCharacterTag


class UserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password', 'raw_password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('raw_password',)


admin.site.register(User, UserAdmin)


class UserCharacterAdmin(admin.ModelAdmin):
    readonly_fields = ('time_added',)


admin.site.register(UserCharacter, UserCharacterAdmin)


admin.site.register(UserCharacterTag)
