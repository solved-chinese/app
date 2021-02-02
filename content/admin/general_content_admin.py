from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse
from django.utils.html import escape

from .utils import NextAdminMixin, DisabledFieldMixin
from content.models import OrderableMixin, AudioFile
from content.question_factories import QuestionFactoryRegistry


__all__ = ['ReviewableAdminMixin', 'GeneralContentAdmin']


@admin.register(AudioFile)
class AudioFileAdmin(DisabledFieldMixin, admin.ModelAdmin):
    list_filter = ('origin', 'type')
    search_fields = ('content__unaccent__iexact',)
    disabled_fields = ('archive',)
    list_display = ('__str__', 'used_in')
    readonly_fields = ('used_in',)

    def used_in(self, audio):
        models = ['radicals', 'characters', 'words', 'sentences']
        links = []
        for model in models:
            for obj in getattr(audio, model).all():
                try:
                    admin_url = obj.get_admin_url()
                except AttributeError:
                    links.append(escape(repr(obj)))
                else:
                    links.append(f"<a href={admin_url}>{escape(repr(obj))}</a>")
        return format_html(', '.join(links))


class ReviewableAdminMixin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return list(readonly_fields) + ['get_review_questions']

    def get_review_questions(self, obj):
        reviewable = obj.get_reviewable_object()
        existing_general_questions = reviewable.questions
        existing_question_types = set()
        s = "<a href='{}'>Reviewable Object</a><br>".format(
            reviewable.get_admin_url())
        for question in existing_general_questions.all():
            s += '<a href="{}">{}</a><br>'.format(
                question.get_admin_url(),
                f"No.{question.order}: {question.question_type}"
            )
            existing_question_types.add(question.question_type)
        for question in QuestionFactoryRegistry.get_factories_by_model(
                obj.__class__):
            if question.question_type not in existing_question_types:
                s += '<a href="{}">generate {}</a><br>'.format(
                    reverse('review_question_factory_view', kwargs={
                        'question_type':question.question_type,
                        'ro_id':obj.get_reviewable_object().id}),
                    question.question_type
                )
        return format_html(s)

    get_review_questions.short_description = "Review Questions"


class GeneralContentAdmin(NextAdminMixin, DisabledFieldMixin, admin.ModelAdmin):
    disabled_fields = ['archive', 'IC_level']
    list_per_page = 50

    def get_exclude(self, request, obj=None):
        """
        not show is_done when creating objects
        """
        exclude = super().get_exclude(request, obj=obj)
        if obj is None:
            exclude = exclude or []
            exclude.append('is_done')
        return exclude

    def get_fields(self, request, obj=None):
        """ overriden to move archive to the end """
        fields = super().get_fields(request, obj=obj).copy()
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
        disabled_fields = super().get_disabled_fields(request, obj=obj)
        if obj is not None and hasattr(obj, 'chinese'):
            return disabled_fields + ['chinese']
        return disabled_fields

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
