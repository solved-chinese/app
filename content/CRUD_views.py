import re

from rest_framework import generics
from rest_framework.response import Response

from content.models import Radical, Character, Sentence, DefinitionInWord, \
    Word, WordSet
from content.serializers import RadicalSerializer, CharacterSerializer, \
    SimpleCharacterSerializer, WordSerializer, \
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

    def retrieve(self, request, *args, **kwargs):
        """ TODO temporary """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        referer = request.META.get('HTTP_REFERER', "")

        word_pattern = r'^.*\/content\/display\/word\/([0-9]+)$'
        word_match = re.match(word_pattern, referer)
        character_pattern = r'^.*\/content\/display\/character\/([0-9]+)$'
        character_match = re.match(character_pattern, referer)

        related_characters = instance.characters.all()
        if character_match:
            character = Character.objects.get(pk=int(character_match.group(1)))
            related_characters = related_characters.exclude(
                pk=character.pk
            )
        elif word_match:
            word = Word.objects.get(pk=int(word_match.group(1)))
            wordset = word.word_sets.first()
            if wordset:
                related_characters = related_characters.filter(
                    word__word_set__pk__lt=wordset.pk
                )
            related_characters = related_characters.difference(
                word.characters.all())
        related_characters = related_characters.distinct()[:RELATED_MAX_NUM]
        data['related_characters'] = SimpleCharacterSerializer(
            list(related_characters), many=True).data
        return Response(data)


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
        pattern = r'^.*\/content\/display\/word\/([0-9]+)$'
        match = re.match(pattern, referer)

        related_words = instance.words.all()
        if match:
            word = Word.objects.get(pk=int(match.group(1)))
            wordset = word.word_sets.first()
            if wordset:
                related_words = instance.words.filter(
                    word_set__pk__lt=wordset.pk
                )
            related_words = related_words.exclude(
                pk=word.pk
            )
        related_words = related_words.distinct()[:RELATED_MAX_NUM]
        data['related_words'] = SimpleWordSerializer(
            list(related_words), many=True).data
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
