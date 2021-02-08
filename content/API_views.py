from uuid import uuid4
import json

from dal import autocomplete
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder

from content.models import GeneralQuestion, LinkedField, Word, Sentence
from learning.models import Record


class QuestionView(APIView):
    """
    Displays and checks answers for questions
    """

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        question_pk = self.kwargs.pop('pk', None)
        self.question = get_object_or_404(GeneralQuestion.objects.all(),
                                          pk=question_pk)

    def get(self, request):
        show_all_options = request.session.get('show_all_options', False)
        client_dict = self.question.render(
            show_all_options=show_all_options
        )
        return Response(client_dict)

    def post(self, request):
        data = request.data.copy()
        is_correct, correct_answer = self.question.check_answer(
            data.get('answer', None))
        # create Record
        user = request.user if request.user.is_authenticated else None
        Record.objects.create(
            action=Record.Action.CORRECT_ANSWER if is_correct
                else Record.Action.WRONG_ANSWER,
            user=user,
            reviewable=self.question.reviewable,
            question=self.question,
            data={
                'answer': data.get('answer', None)
            }
        )
        return Response({
            'is_correct': is_correct,
            'answer': correct_answer,
        })


class LinkedFieldAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, result):
        if self.field_name == '__str__':
            field = str(self.field_name)
        else:
            field = getattr(result, self.field_name)
        return f"{repr(result)}'s {self.field_name}: {field}"

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_staff:
            return LinkedField.objects.none()

        content_type_id = self.forwarded.get('content_type', None)
        self.field_name = self.forwarded.get('field_name', '__str__')
        if content_type_id is None:
            return LinkedField.objects.none()

        model_class = ContentType.objects.get(pk=content_type_id).model_class()
        if model_class in (Word, Sentence):
            self.search_fields = ['chinese']
        else:
            return LinkedField.objects.none()

        if self.field_name in [field.name for field in Word._meta.fields]:
            self.search_fields.append(self.field_name)
        qs = model_class.objects.all()
        qs = self.get_search_results(qs, self.q)
        return qs