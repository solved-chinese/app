from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse

from .utils import NextAdminMixin
from content.models import OrderableMixin
from content.question_factories import QuestionFactoryRegistry


__all__ = ['ReviewableAdminMixin', 'GeneralContentAdmin']


class ReviewableAdminMixin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return list(readonly_fields) + ['get_review_questions']

    def get_review_questions(self, obj):
        reviewable = obj.get_reviewable_object()
        existing_general_questions = reviewable.questions
        existing_question_types = set()
        s = ""
        for question in existing_general_questions.all():
            s += '<a href="{}">{}</a><br>'.format(
                question.get_admin_url(),
                f"{question.question_type}"
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


class GeneralContentAdmin(NextAdminMixin, admin.ModelAdmin):
    disabled_fields = ['archive']
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
        if obj is not None and hasattr(obj, 'chinese'):
            return self.disabled_fields + ['chinese']
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
