from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import ClassSerializer, AssignmentSerializer, \
    AssignmentSimpleSerializer, StudentSerializer, TeacherSerializer
from .models import Class, Assignment, Student, Teacher
from jiezi.rest.permissions import IsTeacher, IsStudent, IsTeacherOrReadOnly


class ClassViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    create: Create class for current teacher
    update: (Note) `student_ids` is used to remove students from a class, it is
    not allowed to add students from the teacher's side.
    """
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]
    queryset = Class.objects.none()  # for API schema generation

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Class.objects.filter(teacher__user=self.request.user)
        return Class.objects.filter(student__user=self.request.user)


class AssignmentViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    create: Create assignment
    """
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.none()  # for API schema generation

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
