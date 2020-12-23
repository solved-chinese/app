from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from content.models import Radical, Character, Sentence, DefinitionInWord, \
    Word, WordSet
from content.serializers import RadicalSerializer, CharacterSerializer, \
    SentenceSerializer, DefinitionInWordSerializer, WordSerializer, \
    WordSetSerializer


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
