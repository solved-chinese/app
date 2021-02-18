import html

from django.views.generic import View
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import user_passes_test

from content.models import GeneralQuestion, Word, \
    ReviewableObject, Radical, Character, WordSet
from .question_factories import QuestionFactoryRegistry, CannotAutoGenerate
from .forms import WordSetSplitForm


class ReviewQuestionFactoryView(View):
    def get(self, request, question_type, ro_id):
        ro = get_object_or_404(ReviewableObject, pk=ro_id)
        factory = QuestionFactoryRegistry.get_factory_by_type(question_type)()
        try:
            general_question = factory.generate(ro)
        except CannotAutoGenerate as e:
            return render(request, 'utils/simple_response.html',
                          {'content': repr(e)})
        return HttpResponseRedirect(general_question.get_admin_url())


class ReviewableObjectDisplayView(DetailView):
    template_name = 'react/learning.html'

    def get_context_data(self, **kwargs):
        return {'react_data': self.object.render()}


class WordDisplayView(ReviewableObjectDisplayView):
    model = Word


class CharacterDisplayView(ReviewableObjectDisplayView):
    model = Character


class RadicalDisplayView(ReviewableObjectDisplayView):
    model = Radical


class SetDisplayView(DetailView):
    model = WordSet
    template_name = 'react/learning.html'

    def get_context_data(self, **kwargs):
        word_pk = self.kwargs.get('word_pk', None)
        wordset = self.object
        all_display = f'You can now preview set "{wordset.name}"<br>'
        words = wordset.words.filter(is_done=True).order_by('wordinset')
        if words.exists():
            if word_pk is None:
                word_pk = words.first().pk
            all_display += ', '.join([
                '<a href="{}" {}>{}</a>'.format(
                    f'/content/display/wordset/{wordset.pk}/{word.pk}',
                    'style="color:red;"' if word_pk == word.pk else "",
                    word.chinese
                )
                for word in words
            ])
        else:
            all_display += "we are not prepared yet, come back later"
            word_pk = Word.objects.filter(is_done=True).first().pk
        context = {
            'pre_react': all_display,
            'react_data': {
                'action': 'display',
                'content': {'type': 'word',
                            'qid': word_pk},
            }
        }
        return context


class QuestionDisplayView(TemplateView):
    template_name = 'react/learning.html'

    def get_context_data(self, **kwargs):
        question_order = self.kwargs.get('question_order', None)
        set_pk = self.kwargs.get('set_pk', None)
        question_pk = self.kwargs.get('question_pk', None)
        if question_pk is not None:
            question_obj = get_object_or_404(GeneralQuestion, pk=question_pk)
        all_display = ""
        if question_order is not None:
            wordset = get_object_or_404(WordSet, pk=set_pk)
            questions = GeneralQuestion.objects.all()
            if question_order != -1:
                questions = questions.filter(order=question_order)
            questions = questions.filter(reviewable__word__word_set=wordset)
            if question_pk is None:
                question_obj = questions.first()
            if question_obj is None:
                raise Http404
            all_display += "You are now viewing questions with order {} in {}<br>"\
                .format(question_order, wordset.name)
            all_display += ", ".join('<a href="{}" {}>{}</a>'.format(
                reverse('question_display',
                        args=(question_order, set_pk, question.pk)),
                'style="color:red;"' if question == question_obj else "",
                html.escape(repr(question.reviewable.word)),
            ) for question in questions.all())
            all_display += '<br><a href="{}">click here to edit this question</a>'\
                .format(question_obj.get_admin_url())
            all_display += '<br><a href="{}">click here to toggle show all options</a>' \
                .format(reverse('show_all_options_toggle'))
        context = {
            'pre_react': all_display,
            'react_data': {
                'action': 'review',
                'content': {'qid': question_obj.pk},
            }
        }
        return context


@user_passes_test(lambda user: user.is_staff)
def show_all_options_toggle(request):
    show_all_options = request.session.get('show_all_options', False)
    show_all_options = not show_all_options
    request.session['show_all_options'] = show_all_options
    return render(request, 'utils/simple_response.html',
                  {'content': f"show all options: {show_all_options}"})


@user_passes_test(lambda user: user.is_superuser)
def split_set_view(request, wordset_pk=None):
    old_wordset = get_object_or_404(WordSet, pk=wordset_pk)
    if request.method == 'POST':
        form = WordSetSplitForm(old_wordset=old_wordset, data=request.POST)
        if form.is_valid():
            wordset = form.save()
            return HttpResponseRedirect(wordset.get_admin_url())
    else:
        form = WordSetSplitForm(old_wordset=old_wordset)
    return render(request, 'utils/form_display.html', {'form': form})
