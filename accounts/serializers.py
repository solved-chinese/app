from rest_framework import serializers
from .models import User

from classroom.serializers import StudentSerializer, TeacherSerializer


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'display_name',
                  'is_teacher', 'is_student', 'student', 'teacher']
