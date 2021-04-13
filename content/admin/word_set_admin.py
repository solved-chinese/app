import html
import pandas as pd

from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import redirect, reverse, render
from django.core.exceptions import ValidationError
from mptt.admin import DraggableMPTTAdmin
from django.db import transaction

from content.models import WordInSet, WordSet, Word, Character, Radical
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
    actions = ['split_wordset', 'rebuild', 'generate_question', 'duplicate',
               'deploy_check', 'display_questions']
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
        result = ""

        objs = [*wordset.words.all(), *Character.objects.filter(word__word_set=wordset)]
        for obj in objs:
            Factories = QuestionFactoryRegistry.get_factories_by_model(obj.__class__)
            factories = [Factory() for Factory in Factories]
            for factory in factories:
                info_string = f"creating {factory.question_type} on {repr(obj)}"
                info_string = html.escape(info_string)
                try:
                    factory.generate(obj.get_reviewable_object())
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

    def deploy_check(self, request, queryset):
        try:
            wordset = queryset.get()
        except (WordSet.MultipleObjectsReturned, WordSet.DoesNotExist):
            self.message_user(request, "can only be done on one set", 'ERROR')
            return
        radicals = Radical.objects.filter(
            character__word__word_set=wordset).distinct()
        characters = Character.objects.filter(
            word__word_set=wordset).distinct()
        words = wordset.words.all()
        results = {}
        for obj in [*radicals, *characters, *words]:
            result = {'obj': html.escape(repr(obj))}
            try:
                obj.clean()
            except ValueError as e:
                result['status'] = f'bad {e!r}'
            else:
                result['status'] = 'good'
            questions = {question for question in
                         obj.get_reviewable_object().questions.all()}
            for factory in QuestionFactoryRegistry \
                    .get_factories_by_model(obj.__class__):
                try:
                    question = next(q for q in questions
                                    if q.question_type == factory.question_type)
                    question.render()
                    if not question.is_done:
                        question_result = 'bad: not done'
                    else:
                        question_result = 'good'
                except StopIteration:
                    question_result = 'bad: not exist'
                except ValidationError as e:
                    question_result = f"bad: {e!r}"
                result[factory.question_type] = html.escape(question_result)
            results.setdefault(obj.__class__.__name__, []).append(result)
        def apply_color(x):
            if x.startswith('good'):
                return 'color: green;'
            elif x.startswith('bad'):
                return 'color: red;'
            return ''
        results = {
            k: pd.DataFrame(v)
                .set_index('obj')
                .style
                .applymap(apply_color)
                .set_table_attributes('class="table"')
                .render()
            for k, v in results.items()
        }
        return render(request,
                      'content/deploy_check.html',
                      {'results': results})

    def display_questions(self, request, queryset):
        try:
            wordset = queryset.get()
        except (WordSet.MultipleObjectsReturned, WordSet.DoesNotExist):
            self.message_user(request, "can only be done on one set", 'ERROR')
            return
        return redirect(reverse('admin_question_display',
                                args=(wordset.jiezi_id,)))
