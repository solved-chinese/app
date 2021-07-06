from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'display_name',
                  'is_teacher', 'is_student']
        read_only_fields = ['pk', 'username', 'is_teacher', 'is_student']
