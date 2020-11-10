from django.contrib import admin
from .models import User


class RemoveTestersFilter(admin.SimpleListFilter):
    # reference https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    title = "Remove Testers"
    parameter_name = 'remove_testers'

    def lookups(self, request, model_admin):
        return (
            (True, 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.model.remove_testers(queryset)
        return queryset


class UserAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'username', 'email', 'is_tester',
                    'last_login')
    list_editable = ('is_tester',)
    list_filter = ('is_teacher', 'is_student', 'is_tester',
                   RemoveTestersFilter)


admin.site.register(User, UserAdmin)
