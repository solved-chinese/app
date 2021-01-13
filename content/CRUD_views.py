import re

from rest_framework import generics
from rest_framework.response import Response

from content.models import Radical, Character, Sentence, DefinitionInWord, \
    Word, WordSet
from content.serializers import RadicalSerializer, CharacterSerializer, \
    SentenceSerializer, DefinitionInWordSerializer, WordSerializer, \
    WordSetSerializer, RELATED_MAX_NUM, SimpleWordSerializer


class WordSetList(generics.ListAPIView):
    """
    __GET__: List all Characters
    """
    queryset = WordSet.objects.all()
    serializer_class = WordSetSerializer


class RadicalDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Character and its related Radical(s)
    """
    queryset = Radical.objects.all()
    serializer_class = RadicalSerializer


class CharacterDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Character and its related Radical(s)
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def retrieve(self, request, *args, **kwargs):
        """ TODO temporary """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        referer = request.META.get('HTTP_REFERER', "")
        pattern = r'^.*\/learning\/display\/\?t=word&qid=([0-9]+)$'
        match = re.match(pattern, referer)
        if match:
            word = Word.objects.get(pk=int(match.group(1)))
            wordset = word.word_sets.first()
            if wordset:
                words = instance.words.filter(
                    word_set__pk__lt=wordset.pk
                ).distinct()[:RELATED_MAX_NUM]
                data['related_words'] = SimpleWordSerializer(
                    list(words), many=True).data
        return Response(data)


class WordDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Character and its related Radical(s)
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordSetDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Character and its related Radical(s)
    """
    queryset = WordSet.objects.all()
    serializer_class = WordSetSerializer
