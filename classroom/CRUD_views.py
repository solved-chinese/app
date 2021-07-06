from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ClassSerializer, AssignmentSerializer, \
    AssignmentListSerializer, StudentSerializer, TeacherSerializer
from .models import Class, Assignment, Student, Teacher
from jiezi.rest.permissions import IsTeacher, IsStudent, IsTeacherOrReadOnly


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


class StudentDetail(generics.RetrieveUpdateAPIView):
    """
    (Note) use `class_code` to set the class of the student,
    set to null to quit the current class
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_object(self):
        return Student.of(self.request.user)


class TeacherDetail(generics.RetrieveAPIView):
    """
    (Note) Use class-list and class-detail page for class manipulations
    """
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self):
        return Teacher.of(self.request.user)
