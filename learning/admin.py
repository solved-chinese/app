import json

from django.db.models import Q
from django.utils.html import format_html
from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin

from .models import Record
from jiezi.utils.admins import ViewOnlyAdminMixin
from accounts.admin import user_linked_display
from content.question_factories import QuestionFactoryRegistry


class QuestionTypeListFilter(admin.SimpleListFilter):
    title = 'Question Type'
    parameter_name = 'question_type'

    def lookups(self, request, model_admin):
        return ((t, t) for t in QuestionFactoryRegistry.type_list())

    def queryset(self, request, queryset):
        value = self.value()
        return queryset.filter(
            Q(question__MC__question_type=value)
            | Q(question__FITB__question_type=value)
            | Q(question__CND__question_type=value)
        )


@admin.register(Record)
class RecordAdmin(AdminAdvancedFiltersMixin, ViewOnlyAdminMixin,
                  admin.ModelAdmin):
    list_display = ('get_user', 'time', 'action', 'reviewable',
                    'get_question', 'get_set_name', 'get_answer')
    list_display_links = ('action',)
    list_filter = (
        'action',
        QuestionTypeListFilter,
        ('user__student__klass', admin.RelatedOnlyFieldListFilter),
        ('learning_process__wordset', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('user__username__exact',)
    exclude = ('data', 'question')
    readonly_fields = ('get_data', 'get_question')
    advanced_filter_fields = (
        'user__display_name', 'user__alias',
        ('reviewable__word__id', 'word_id'),
        ('reviewable__word__chinese', 'word_chinese'),
        ('reviewable__character__id', 'char_id'),
        ('reviewable__character__chinese', 'char_chinese'),
        ('reviewable__radical__id', 'rad_id'),
        ('reviewable__radical__chinese', 'rad_chinese'),
        'action',
    )
    list_per_page = 50
    list_select_related = ('user__student__klass', 'user__teacher', 'question',
                           'learning_process__wordset')

    def get_user(self, record):
        if record.user:
            return user_linked_display(record.user)
        return 'None'

    def get_question(self, record):
        if record.question:
            return format_html(
                "<a href={}>{}</a>",
                record.question.get_admin_url(),
                record.question.question_form)
        else:
            return None

    def get_answer(self, record):
        return record.data.get('answer', None)

    def get_data(self, record):
        data = json.dumps(record.data, ensure_ascii=False, indent=4)
        return data

    def get_set_name(self, record):
        try:
            return record.learning_process.wordset.name
        except AttributeError:
            return '--'
