class DisabledFieldMixin:
    disabled_fields = ()

    def get_disabled_fields(self, request, obj=None):
        """ Get the list of fields to disable in form
            disable chinese editing in change form
         """
        return self.disabled_fields

    def get_form(self, request, obj=None, **kwargs):
        """ This is overriden to disable the fields in form according to
        the get_disabled_fields() """
        form = super().get_form(request, obj=obj, **kwargs)
        for field_name in self.get_disabled_fields(request, obj=obj):
            try:
                form.base_fields[field_name].disabled = True
            except KeyError:
                pass
        return form
