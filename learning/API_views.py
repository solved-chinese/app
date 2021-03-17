from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


from content.models import WordSet, ReviewableObject
from learning.models.learning_algorithm import LearningProcess


class LearningAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)
        self.process = LearningProcess.of(request.user, self.wordset)

    def post(self, request):
        data = request.data.copy()
        self.process.request = request
        return Response(self.process.get_response(data))


class AssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        set_pk = self.kwargs.pop('set_pk', None)
        self.wordset = get_object_or_404(WordSet, pk=set_pk)
        self.process = LearningProcess.of(request.user, self.wordset)

    def get(self, request):
        render = lambda obj: {
            'type': obj.concrete_object.__class__.__name__.lower(),
            'qid': obj.concrete_object.id,
            'pinyin': obj.concrete_object.pinyin,
            'chinese': obj.radical.image.url if obj.radical
                else obj.concrete_object.chinese,
            'definition': obj.definition,
            'status': 'mastered' if obj.pk in self.process.data['mastered_list']
                else 'familiar' if obj.pk in self.process.data['review_list']
                else 'remaining',
        }
        word_reviewables = map(
            lambda wis: wis.word.get_reviewable_object(),
            self.wordset.wordinset_set.all().prefetch_related(
                'word__definitions')
        )

        bonus_reviewables = ReviewableObject.objects.filter(
            pk__in=self.process.data['bonus_list']).prefetch_related(
            'character__definitions').select_related('radical')
        character_list = filter(lambda obj: obj and obj.character,
                                bonus_reviewables)
        radical_list = filter(lambda obj: obj and obj.radical,
                              bonus_reviewables)
        response = {
            'name': self.wordset.name,
            'progressBar': self.process.data['progress_bar'],
            'word_list': map(render, word_reviewables),
            'character_list': map(render, character_list),
            'radical_list': map(render, radical_list),
        }
        return Response(response)
