from django.contrib import admin
from .models import User


class RemoveTestersFilter(admin.SimpleListFilter):
    # reference https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    title = "Remove Testers"
    parameter_name = 'remove_testers'
    default_filter = 'actual'

    def lookups(self, request, model_admin):
        return (
            (self.default_filter, 'Only Actualy Users'),
            ('all', 'All users'),
            ('testers', 'Only testers'),
        )

    def choices(self, cl):
        """ this is used to remove the all default tag """
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup if self.value()
                    else (True if lookup == self.default_filter else False),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == self.default_filter or self.value() is None:
            return queryset.model.remove_testers(queryset)
        elif self.value() == 'all':
            return queryset
        elif self.value() == 'testers':
            actual = queryset.model.remove_testers(queryset)
            return queryset.exclude(pk__in=actual)
        raise Exception('should get here')


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
