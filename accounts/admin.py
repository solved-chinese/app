from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('display_name', 'email')}),
        ('Solved specific info', {'fields': ('is_student', 'is_teacher')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'display_name', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'is_student', 'is_teacher')
    search_fields = ('username', 'display_name', 'email')
