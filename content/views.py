from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from dal import autocomplete

from uuid import uuid4
from content.models import GeneralQuestion, LinkedField, ContentType, Word, \
    ReviewableObject, Sentence
from .question_factories import QuestionFactoryRegistry, CannotAutoGenerate


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
        client_dict, server_dict = self.question.render()
        question_id = uuid4().hex
        client_dict = {
            "id": question_id,
            "form": self.question.question_form,
            "content": client_dict,
        }
        server_dict.update({
            "id": question_id,
            "start_time": timezone.now(),
            "question_pk": self.question.pk,
        })
        request.session['question'] = server_dict
        return Response(client_dict)

    def post(self, request):
        server_dict = request.session.get('question', None)
        data = request.data.copy()
        question_id = data.pop('id', None)
        if server_dict is None \
                or question_id != server_dict.get('id', None) \
                or self.question.pk != server_dict.get('question_pk', None):
            return Response(status=status.HTTP_409_CONFLICT)
        response_dict, is_correct = self.question.check_answer(data,
                                                               server_dict)
        return Response(response_dict)


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


class ReviewQuestionFactoryView(View):
    def get(self, request, question_type, ro_id):
        ro = get_object_or_404(ReviewableObject, pk=ro_id)
        factory = QuestionFactoryRegistry.get_factory_by_type(question_type)
        try:
            general_question = factory.generate(ro)
        except CannotAutoGenerate as e:
            return render(request, 'utils/simple_response.html',
                          {'content': repr(e)})
        return HttpResponseRedirect(general_question.get_admin_url())
