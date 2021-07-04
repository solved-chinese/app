from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    __GET__ : Retrieves the detail of current User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
