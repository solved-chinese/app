from django.contrib import admin

from content.models import OrderableMixin


class GeneralContentAdmin(admin.ModelAdmin):
    disabled_fields = ['archive']

    def get_fields(self, request, obj=None):
        """ overriden to move archive to the end """
        fields = super().get_fields(request, obj=None).copy()
        try:
            index = fields.index('archive')
        except ValueError:
            return fields
        fields.pop(index)
        return [*fields, 'archive']

    def get_disabled_fields(self, request, obj=None):
        """ Get the list of fields to disable in form
            disable chinese editing in change form
         """
        if obj is not None and hasattr(obj, 'chinese'):
            return self.disabled_fields + ['chinese']
        return self.disabled_fields

    def get_form(self, request, obj=None, **kwargs):
        """ This is overriden to disable the fields in form according to
        the get_disabled_fields() """
        form = super().get_form(request, obj=obj, **kwargs)
        for field_name in self.get_disabled_fields(request, obj=obj):
            form.base_fields[field_name].disabled = True
        return form

    def save_formset(self, request, form, formset, change):
        """ make sure the order is correct when editor doesn't specify """
        if issubclass(formset.model, OrderableMixin):
            for index, form in enumerate(formset):
                form.instance.order += index * 1e-9
        super().save_formset(request, form, formset, change)

    def save_related(self, request, form, formsets, change):
        """ reset the order to be 0,1,2... """
        super().save_related(request, form, formsets, change)
        form.instance.reset_order()
