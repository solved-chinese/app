from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from content.models import WordSet


class LearningView(LoginRequiredMixin, TemplateView):
    template_name = 'react/learning.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)

    def get_context_data(self, **kwargs):
        return {
            'react_data': {
                'action': 'learning',
                'content': {
                    'qid': self.wordset.pk
                }
            }
        }


class AssignmentView(LoginRequiredMixin, TemplateView):
    template_name = 'react/learning.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)

    def get_context_data(self, **kwargs):
        return {
            'react_data': {
                'action': 'assignment',
                'content': {
                    'qid': self.wordset.pk
                }
            }
        }
