from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TeacherSerializer, StudentSerializer, ClassSerializer, \
    AssignmentSerializer, AssignmentListSerializer, AssignmentUpdateSerializer
from .models import Class, Assignment
from jiezi.rest.permissions import IsTeacher, IsTeacherOrReadOnly


class ClassCreate(generics.CreateAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Class.objects.filter(teacher__user=self.request.user)
        return Class.objects.filter(student__user=self.request.user)


# TODO unify assignment serializers & remove hacks
class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Assignment.objects.filter(klass__teacher__user=self.request.user)
        return Assignment.objects.filter(klass__student__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AssignmentSerializer
        return AssignmentUpdateSerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = AssignmentSerializer(instance=instance,
                                          context={'request': request})
        return Response(serializer.data)


class AssignmentCreate(generics.CreateAPIView):
    serializer_class = AssignmentUpdateSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        serializer = AssignmentSerializer(instance=instance,
                                          context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
