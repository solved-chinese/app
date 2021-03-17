import logging
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import mail_managers
from django.db.models import ObjectDoesNotExist

from content.models import WordSet
from classroom.models import Assignment


class LearningView(LoginRequiredMixin, TemplateView):
    template_name = 'react/learning.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)

    def get_context_data(self, **kwargs):
        # notify managers if an assignment is started
        # requirements: class with more than 2 students
        if self.request.user.is_student:
            try:
                assignment = Assignment.objects.get(
                    wordset=self.wordset,
                    klass=self.request.user.student.klass,
                )
            except ObjectDoesNotExist:
                logger.error(exc_info=True)
            else:
                from jiezi.settings import DEBUG
                if (not DEBUG
                        and not assignment.data.get('managers_notified', False)
                        and assignment.klass.students.count() > 2):
                    logger.info("send info")
                    mail_managers(f'Students started on {repr(assignment)}',
                                  'one student has started learning',
                                  fail_silently=True)

        return {
            'react_data': {
                'action': 'learning',
                'content': {
                    'qid': self.wordset.pk
                }
            }
        }


class AssignmentView(LoginRequiredMixin, TemplateView):
    template_name = 'react/assignment.html'

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
