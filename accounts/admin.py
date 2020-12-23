from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'username', 'email', 'last_login',
                    'is_staff')
    list_filter = ['is_staff']
    search_fields = ['display_name', 'username', 'email']
