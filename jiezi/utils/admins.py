from django.shortcuts import reverse


class ViewOnlyAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


def get_admin_url(obj):
    return reverse('admin:{}_{}_change'.format(
        obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
