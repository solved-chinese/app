from rest_framework import serializers

from classroom.models import Student, Class, Assignment


__all__ = ['StudentSimpleSerializer', 'ClassSimpleSerializer',
           'AssignmentSimpleSerializer']


class StudentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['display_name', 'pk']


class ClassSimpleSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(read_only=True,
                                           slug_field='display_name')

    class Meta:
        model = Class
        fields = ['url', 'pk', 'name', 'code', 'teacher']


class AssignmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'pk', 'url']