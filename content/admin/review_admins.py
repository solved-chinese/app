from django.contrib import admin
from django.db import models
from django.shortcuts import HttpResponseRedirect

from content.models import GeneralQuestion, ReviewableObject, MCChoice, \
    LinkedField, MCQuestion, FITBQuestion, CNDQuestion
from content.forms import LinkedFieldForm
from .utils import DisabledFieldMixin


__all__ = ['FITBAdmin', 'MCChoiceInlineAdmin', 'MCQuestionAdmin']


class GeneralReviewQuestionAdmin(DisabledFieldMixin, admin.ModelAdmin):
    def get_disabled_fields(self, request, obj=None):
        disabled_fields = list(super().get_disabled_fields(request, obj=obj))
        disabled_fields.extend(['reviewable', 'question_type'])
        for field in self.model._meta.fields:
            if isinstance(field, models.ForeignKey) and \
                    field.related_model == LinkedField: # including 1-to-1
                disabled_fields.append(field.name)
        return disabled_fields


@admin.register(FITBQuestion, CNDQuestion)
class FITBAdmin(GeneralReviewQuestionAdmin):
    pass


class GeneralQuestionInlineAdmin(admin.TabularInline):
    model = GeneralQuestion
    extra = 0


@admin.register(ReviewableObject)
class ReviwableObjectAdmin(DisabledFieldMixin, admin.ModelAdmin):
    disabled_fields = ('radical', 'character', 'word')
    inlines = [GeneralQuestionInlineAdmin]


@admin.register(LinkedField)
class LinkedFieldAdmin(admin.ModelAdmin):
    form = LinkedFieldForm


@admin.register(GeneralQuestion)
class GeneralQuestionAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.model.objects.get(pk=object_id)
        return HttpResponseRedirect(obj.concrete_question.get_admin_url())

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class MCChoiceInlineAdmin(admin.TabularInline):
    model = MCChoice
    fields = ['linked_value', 'get_value', 'weight']
    readonly_fields = ['get_value']
    extra = 0

    def get_value(self, obj):
        return obj.value


@admin.register(MCQuestion)
class MCQuestionAdmin(GeneralReviewQuestionAdmin):
    model = MCQuestion
    inlines = [MCChoiceInlineAdmin]
