import html

from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import redirect, reverse, render
from mptt.admin import DraggableMPTTAdmin
from django.db import transaction

from content.models import WordInSet, WordSet, Word
from content.admin import GeneralContentAdmin
from content.forms import WordSetCreationForm
from content.question_factories.question_factory_registry \
    import QuestionFactoryRegistry


class WordInSetInline(admin.TabularInline):
    model = WordInSet
    autocomplete_fields = ['word']
    readonly_fields = ['is_done', 'get_definitions']
    extra = 0

    def is_done(self, obj):
        return '\u2705' if obj.word.is_done else '\u274c'

    def get_definitions(self, wiws):
        w = wiws.word
        definitions = ""
        for d in w.definitions.all():
            definitions += f"{d.part_of_speech} {d.definition}; "
        return definitions


@admin.register(WordSet)
class WordSetAdmin(DraggableMPTTAdmin, GeneralContentAdmin):
    list_display = ['tree_actions', 'indented_title', 'jiezi_id', 'is_done']
    list_editable = ['jiezi_id', 'is_done']
    list_display_links = ('indented_title',)
    list_filter = ['is_done']
    search_fields = ['name__search']
    readonly_fields = ['lft', 'rght', 'tree_id']
    actions = ['split_wordset', 'rebuild', 'generate_question', 'duplicate']
    inlines = [WordInSetInline]
    mptt_level_indent = 30
    save_as = True

    def get_form(self, request, obj=None, **kwargs):
        """
        User a special from for creation
        reference django.contrib.auth.admin.UserAdmin.get_form
        """
        defaults = {}
        if obj is None:
            defaults['form'] = WordSetCreationForm
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def split_wordset(self, request, queryset):
        qs_cnt = queryset.count()
        if qs_cnt != 1:
            self.message_user(request,
                              f"error: can select only 1 but {qs_cnt} received")
            return
        return redirect(reverse('split_wordset', args=(queryset.get().pk,)))

    def rebuild(self, request, queryset):
        WordSet.objects.rebuild()

    def generate_question(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "can only generate question for "
                                       "one wordset", 'ERROR')
            return

        wordset = queryset.get()
        Factories = QuestionFactoryRegistry.get_factories_by_model(Word)
        factories = [Factory() for Factory in Factories]
        result = ""

        for word in wordset.words.all():
            for factory in factories:
                info_string = f"creating {factory.question_type} on {repr(word)}"
                info_string = html.escape(info_string)
                try:
                    factory.generate(word.get_reviewable_object())
                except Exception as e:
                    result += f'<div style="color: red">fail {info_string} ' \
                              f'{html.escape(repr(e))}</div>'
                else:
                    result += f'<div style="color: green">good {info_string}</div>'
        return render(request, 'utils/simple_response.html',
                      {'content': format_html(result)})

    @transaction.atomic
    def duplicate(self, request, queryset):
        try:
            obj = queryset.get()
        except (WordSet.MultipleObjectsReturned, WordSet.DoesNotExist):
            self.message_user(request, "can only be done on one set", 'ERROR')
            return
        old_pk = obj.pk
        obj.pk = None
        obj.jiezi_id += '-copy'
        obj.name += '-copy'
        obj.save()
        for wis in WordInSet.objects.filter(word_set=old_pk):
            wis.pk = None
            wis.word_set = obj
            wis.save()
