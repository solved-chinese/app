from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk',
                  'username', 'first_name', 'last_name', 'email',
                  'is_guest', 'is_teacher', 'is_student']
