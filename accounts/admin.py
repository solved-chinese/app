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


class RemoveTestersRelatedOnlyFieldListFilter(admin.RelatedFieldListFilter):
    """ modified from admin.RelatedOnlyFieldListFilter """
    def field_choices(self, field, request, model_admin):
        qs = model_admin.get_queryset(request)
        qs = qs.model.remove_testers(qs)
        pk_qs = qs.distinct().values_list('%s__pk' % self.field_path, flat=True)
        ordering = self.field_admin_ordering(field, request, model_admin)
        return field.get_choices(include_blank=False,
                                 limit_choices_to={'pk__in': pk_qs},
                                 ordering=ordering)


class UserAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'username', 'email', 'is_tester',
                    'last_login')
    list_editable = ('is_tester',)
    list_filter = ('is_teacher', 'is_student', 'is_tester',
                   RemoveTestersFilter)
    search_fields = ['display_name', 'username', 'email']


admin.site.register(User, UserAdmin)
