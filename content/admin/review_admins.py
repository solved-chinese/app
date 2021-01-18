from django.contrib import admin
from django.db import models

from content.models import GeneralQuestion, ReviewableObject, MCChoice, \
    LinkedField, MCQuestion, FITBQuestion
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


@admin.register(FITBQuestion)
class FITBAdmin(GeneralReviewQuestionAdmin):
    pass


@admin.register(LinkedField)
class LinkedFieldAdmin(admin.ModelAdmin):
    form = LinkedFieldForm


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
