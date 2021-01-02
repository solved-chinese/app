from django.contrib import admin


class GeneralContentAdmin(admin.ModelAdmin):
    disabled_fields = ['archive']

    def get_disabled_fields(self, request, obj=None):
        """ Get the list of fields to disable in form """
        disabled_fields = self.disabled_fields
        if obj is not None:
            try:
                getattr(obj, 'chinese')
                disabled_fields += ['chinese']
            except AttributeError:
                pass
        return disabled_fields

    def get_form(self, request, obj=None, **kwargs):
        """ This is overriden to disable the fields in form according to
        the get_disabled_fields() """
        form = super().get_form(request, obj=obj, **kwargs)
        for field_name in self.get_disabled_fields(request, obj=obj):
            form.base_fields[field_name].disabled = True
        return form

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.reset_order()
