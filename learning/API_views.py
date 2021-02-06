from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from content.models import WordSet
from learning.models.learning_algorithm import LearningProcess


class LearningAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)
        self.process= LearningProcess.of(request.user, self.wordset)

    def post(self, request):
        data = request.data.copy()
        return Response(self.process.get_response(data))
