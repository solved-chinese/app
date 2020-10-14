from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content.models import CharacterSet
from jiezi.rest.permissions import IsOwnerStudent, IsStudent
from learning.models import StudentCharacter, StudentCharacterTag
from learning.serializers import StudentCharacterSimpleSerializer, \
    StudentCharacterSerializer, StudentCharacterTagSerializer


class StudentCharacterList(generics.ListAPIView):
    """
    __GET__: Lists all UserCharacters belonging to current User
    """
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StudentCharacterSimpleSerializer

    def get_queryset(self):
        return self.request.user.student.student_characters


class StudentCharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    __GET__ / __PUT__ / __DELETE__: Retrieve / update / destroy the detail
    of a StudentCharacter belonging to current user
    """
    permission_classes = [IsAuthenticated, IsStudent, IsOwnerStudent]
    queryset = StudentCharacter.objects.all()
    serializer_class = StudentCharacterSerializer


class StudentCharacterTagList(generics.ListCreateAPIView):
    """
    __GET__: Lists all user character tags belonging to current user

    __POST__: Add a StudentCharacterTag linked to a CharacterSet with the given
    `character_set_id`. This CharacterSet must not be added to this user
    before.
    """
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StudentCharacterTagSerializer

    def create(self, request, *args, **kwargs):
        cset_pk = request.data['character_set_id']
        cset = CharacterSet.objects.get(pk=cset_pk)
        obj = StudentCharacterTag.objects.create(character_set=cset,
                                                 student=request.user.student)
        obj.update_from_character_set()
        data = StudentCharacterTagSerializer(
            obj, context=self.get_serializer_context()).data
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers={'Location': str(data['url'])})

    def get_queryset(self):
        return self.request.user.student.sc_tags

    POST_action = {
        'character_set_id' : {
            'type' : 'integer',
            'example' : 1,
        }
    }


class StudentCharacterTagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    __GET__ / __PUT__ / __DELETE__ : Retrieves / update / destroy the detail of
    a StudentCharacterTag belonging to the current User
    """
    permission_classes = [IsAuthenticated, IsStudent, IsOwnerStudent]
    queryset = StudentCharacterTag.objects.all()
    serializer_class = StudentCharacterTagSerializer
