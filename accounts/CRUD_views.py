from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from jiezi.rest.permissions import IsOwner
from .serializers import UserSerializer, UserCharacterSerializer, \
    UserCharacterTagSerializer, UserCharacterSimpleSerializer
from learning.models import CharacterSet
from accounts.models import UserCharacter, UserCharacterTag


class MyUserDetail(generics.RetrieveUpdateAPIView):
    """
    __GET__ / __PUT__ : Retrieves / update the detail of current User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserCharacterList(generics.ListAPIView):
    """
    __GET__: Lists all UserCharacters belonging to current User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserCharacterSimpleSerializer

    def get_queryset(self):
        return self.request.user.user_characters


class UserCharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    __GET__ / __PUT__ / __DELETE__: Retrieve / update / destroy the detail
    of a UserCharacter belonging to current user
    """
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = UserCharacter.objects.all()
    serializer_class = UserCharacterSerializer


class UserCharacterTagList(generics.ListCreateAPIView):
    """
    __GET__: Lists all user character tags belonging to current user

    __POST__: Add a UserCharacterTag linked to a CharacterSet with the given
    `character_set_id`. This CharacterSet must not be added to this user
    before.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserCharacterTagSerializer

    def create(self, request, *args, **kwargs):
        cset_pk = request.data['character_set_id']
        cset = CharacterSet.objects.get(pk=cset_pk)
        obj = UserCharacterTag.objects.create(character_set=cset,
                                              user=request.user)
        obj.update_from_character_set()
        data = UserCharacterTagSerializer(
            obj, context=self.get_serializer_context()).data
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers={'Location': str(data['url'])})

    def get_queryset(self):
        return self.request.user.user_character_tags

    POST_action = {
        'character_set_id' : {
            'type' : 'integer',
            'example' : 1,
        }
    }


class UserCharacterTagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & IsOwner]
    queryset = UserCharacterTag.objects.all()
    serializer_class = UserCharacterTagSerializer
