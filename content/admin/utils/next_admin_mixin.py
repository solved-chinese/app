# modified from https://stackoverflow.com/questions/58014139/how-to-go-to-next-object-in-django-admin

from django.http import QueryDict
from django.shortcuts import redirect


class NextAdminMixin():
    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = {}
        context.update(extra_context or {})
        context['show_save_and_add_another'] = False
        querystring = request.GET.get('_changelist_filters')
        if querystring:
            context['show_save_and_next'] = True
        return super().change_view(request, object_id, form_url, context)

    def get_next_instance_pk(self, request, current):
        """
        Returns the primary key of the next object in the query
        (considering filters and ordering).
        Returns None if the object is not in the queryset.
        """
        querystring = request.GET.get('_changelist_filters')
        if querystring:
            # Alters the HttpRequest object to make it function as a list request
            original_get = request.GET
            try:
                request.GET = QueryDict(querystring)
                # from django.contrib.admin.options: ModelAdmin.changelist_view
                ChangeList = self.get_changelist(request)
                list_display = self.get_list_display(request)
                changelist = ChangeList(
                    request, self.model, list_display,
                    self.get_list_display_links(request, list_display),
                    self.get_list_filter(request),
                    self.date_hierarchy,
                    self.get_search_fields(request),
                    self.get_list_select_related(request),
                    self.list_per_page,
                    self.list_max_show_all,
                    self.list_editable,
                    self,
                    self.sortable_by)  # New in Django 2.0
                queryset = changelist.get_queryset(request)
            finally:
                request.GET = original_get
        else:
            queryset = self.get_queryset(request)

        # Try to find pk in this list:
        iterator = queryset.values_list('pk', flat=True).iterator()
        try:
            while next(iterator) != current.pk:
                continue
            return next(iterator)
        except StopIteration:
            return None # Not found or it was the last item

    def response_change(self, request, obj):
        """Determines the HttpResponse for the change_view stage."""
        if '_save_next' in request.POST:
            next_pk = self.get_next_instance_pk(request, obj)
            app = obj._meta.app_label
            model = obj._meta.model_name
            if next_pk:
                response = redirect(f'admin:{app}_{model}_change', next_pk)
                qs = request.GET.urlencode()  # keeps _changelist_filters
            else:
                # Last item (or no longer in list) - go back to list in the same position
                response = redirect(f'admin:{app}_{model}_changelist')
                qs = request.GET.get('_changelist_filters')

            if qs:
                response['Location'] += '?' + qs
            return response

        return super().response_change(request, obj)
