from rest_framework import generics
from rest_framework.response import Response
from django.db.models import F

from content.models import Radical, Character, Sentence, DefinitionInWord, \
    Word, WordSet
from content.serializers import RadicalSerializer, CharacterSerializer, \
    SimpleCharacterSerializer, WordSerializer, SimpleWordSetSerializer, \
    WordSetSerializer, RELATED_MAX_NUM, SimpleWordSerializer


class WordSetList(generics.ListAPIView):
    """
    List all done wordsets
    """
    serializer_class = SimpleWordSetSerializer

    def get_queryset(self):
        return WordSet.objects.filter(is_done=True)


class RadicalDetail(generics.RetrieveAPIView):
    queryset = Radical.objects.all()
    serializer_class = RadicalSerializer


class CharacterDetail(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def retrieve(self, request, *args, **kwargs):
        """ TODO temporary """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        related_characters = Character.objects\
            .filter(radicals__in=instance.radicals.all(), is_done=True)\
            .exclude(pk=instance.pk)\
            .distinct()\
            .order_by(F('IC_level').desc(nulls_last=True))[:RELATED_MAX_NUM]
        data['related_characters'] = SimpleCharacterSerializer(
            list(related_characters),
            many=True,
            context={'request': request}
        ).data
        return Response(data)


class WordDetail(generics.RetrieveAPIView):
    """
    Word detail, **different for single-char word**

    For single char word, give a list of a length 1, containing radical
    urls separated by semicolon.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def retrieve(self, request, *args, **kwargs):
        """ TODO temporary """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        related_words = Word.objects \
            .filter(characters__in=instance.characters.all(), is_done=True) \
            .exclude(pk=instance.pk) \
            .distinct() \
            .order_by(F('IC_level').desc(nulls_last=True))[:RELATED_MAX_NUM]
        data['related_words'] = SimpleWordSerializer(
            list(related_words),
            many=True,
            context={'request': request}
        ).data
        return Response(data)


class WordSetDetail(generics.RetrieveAPIView):
    """
    (Note) Word sets use a tree structure, for details
    reference https://www.ibase.ru/files/articles/programming/dbmstrees/sqltrees.html,
    tell me if there needs to be a better representation of this
    """
    queryset = WordSet.objects.all()
    serializer_class = WordSetSerializer
