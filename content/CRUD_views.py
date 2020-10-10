from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from content.models import Character, Radical, CharacterSet
from content.serializers import SimpleCharacterSerializer, CharacterSerializer, \
    SimpleRadicalSerializer, RadicalSerializer, CharacterSetSerializer


class CharacterList(generics.ListAPIView):
    """
    __GET__: List all Characters
    """
    queryset = Character.objects.all()
    serializer_class = SimpleCharacterSerializer


class CharacterDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Character and its related Radical(s)
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class RadicalList(generics.ListAPIView):
    """
    __GET__: List all Radicals
    """
    queryset = Radical.objects.all()
    serializer_class = SimpleRadicalSerializer


class RadicalDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a Radical
    """
    queryset = Radical.objects.all()
    serializer_class = RadicalSerializer


class CharacterSetList(generics.ListAPIView):
    """
    __GET__: List all character sets that have not been added to current User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSetSerializer

    def get_queryset(self):
        return CharacterSet.objects.exclude(
            user_character_tag__in=self.request.user.user_character_tags.all())


class CharacterSetDetail(generics.RetrieveAPIView):
    """
    __GET__: Retrieve the detail of a CharacterSet
    """
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
