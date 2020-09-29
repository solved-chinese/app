from rest_framework import serializers
from .models import Character, Radical, CharacterSet


class RadicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radical
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class CharacterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSet
        fields = '__all__'
