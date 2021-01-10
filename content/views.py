from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from uuid import uuid4
from content.models import GeneralQuestion


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
        client_dict['id'] = question_id
        server_dict['id'] = question_id
        server_dict['start_time'] = timezone.now()
        server_dict['question_pk'] = self.question.pk
        request.session['question'] = server_dict
        return Response(client_dict)

    def post(self, request):
        server_dict = request.session.get('question', None)
        question_id = request.data.pop('id', None)
        if server_dict is None \
                or question_id != server_dict.get('id', None) \
                or self.question.pk != server_dict.get('question_pk', None):
            return Response(status=status.HTTP_409_CONFLICT)
        response_dict, is_correct = self.question.check_answer(request.data,
                                                               server_dict)
        return Response(response_dict)
