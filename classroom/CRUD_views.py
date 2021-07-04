from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import ClassSerializer, AssignmentSerializer, \
    AssignmentListSerializer
from .models import Class, Assignment
from jiezi.rest.permissions import IsTeacher, IsTeacherOrReadOnly


class ClassCreate(generics.CreateAPIView):
    """
    Create class for current teacher
    """
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


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    list: List all related assignments
    create: Create assignment
    """
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return AssignmentListSerializer
        return AssignmentSerializer

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Assignment.objects.filter(klass__teacher__user=self.request.user)
        return Assignment.objects.filter(klass__student__user=self.request.user)
