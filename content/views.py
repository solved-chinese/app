from django.views.generic import View
from django.http import HttpResponseRedirect, Http404
from django.views.generic import DetailView, TemplateView
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

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
        context = {
            'react_data': {
                'action': 'review',
                'content': {'qid': kwargs.get('question_pk', 0)},
            }
        }
        return context


@user_passes_test(lambda user: user.is_staff)
def admin_display_question(request, set_pk, question_pk=None):
    if request.method == 'POST':
        question = get_object_or_404(GeneralQuestion,
                                     pk=request.POST.get('question_pk', None))
        question.concrete_question.is_done ^= True
        question.concrete_question.save()

    if set_pk.isnumeric():
        wordset = get_object_or_404(WordSet, pk=set_pk)
    else:
        wordset = get_object_or_404(WordSet, jiezi_id__iexact=set_pk)
    questions = GeneralQuestion.objects.all()
    questions = questions.filter(
        Q(reviewable__word__word_set=wordset)
        | Q(reviewable__character__word__word_set=wordset)
        | Q(reviewable__radical__character__word__word_set=wordset)
    ).distinct()
    questions = questions.select_related('MC', 'FITB', 'CND')
    questions_by_type = {}
    for question in questions:
        questions_by_type.setdefault(question.question_type, []).append(question)
    if question_pk is None:
        current_question = questions.first()
    else:
        current_question = get_object_or_404(GeneralQuestion, pk=question_pk)
    context = {
        'set_pk': set_pk,
        'questions_by_type': questions_by_type,
        'current_question': current_question,
    }
    return render(request, 'react/question_list.html', context)


def search_view(request):
    context = {
        'react_data': {
            'action': 'search',
            'content': {},
        }
    }
    return render(request, 'react/search.html', context=context)


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
