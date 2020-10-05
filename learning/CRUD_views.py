from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from learning.serializers import CharacterSerializer, CharacterSetSerializer, \
    RadicalSerializer, SimpleCharacterSerializer, SimpleRadicalSerializer
from learning.models import Character, CharacterSet, Radical


class CharacterList(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = SimpleCharacterSerializer


class CharacterDetail(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class RadicalList(generics.ListAPIView):
    queryset = Radical.objects.all()
    serializer_class = SimpleRadicalSerializer


class RadicalDetail(generics.RetrieveAPIView):
    queryset = Radical.objects.all()
    serializer_class = RadicalSerializer


class CharacterSetList(generics.ListAPIView):
    """
    This api returns all character sets that have not been added to the user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSetSerializer

    def get_queryset(self):
        return CharacterSet.objects.exclude(
            user_character_tag__in=self.request.user.user_character_tags.all())


class CharacterSetDetail(generics.RetrieveAPIView):
    queryset = CharacterSet.objects.all()
    serializer_class = CharacterSetSerializer
