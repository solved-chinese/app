from django.contrib import admin

from content.models import GeneralQuestion, ReviewableObject, MCChoice, \
    LinkedField, MCQuestion
from content.forms import LinkedFieldForm


__all__ = ['GeneralAdmin', 'MCChoiceInlineAdmin', 'MCQuestionAdmin']


@admin.register(ReviewableObject, GeneralQuestion)
class GeneralAdmin(admin.ModelAdmin):
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
class MCQuestionAdmin(admin.ModelAdmin):
    model = MCQuestion
    inlines = [MCChoiceInlineAdmin]
