from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'action', 'reviewable',
                    'question', 'get_set_name')
    list_filter = ( 'learning_process__wordset__name',)
    search_fields = ('user__username__exact',)

    def get_set_name(self, record):
        try:
            return record.learning_process.wordset.name
        except AttributeError:
            return '--'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
