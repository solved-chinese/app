from rest_framework import serializers
from content.serializers import CharacterSerializer
from learning.models import StudentCharacter, StudentCharacterTag


class StudentCharacterSimpleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='student_character_detail')

    class Meta:
        model = StudentCharacter
        fields = ['pk', 'url']


class StudentCharacterSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = StudentCharacter
        fields = ['pk', 'character', 'state']


class StudentCharacterTagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='student_character_tag_detail')
    states_count = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    student_characters = serializers.HyperlinkedRelatedField(
        many=True, queryset=StudentCharacter.objects.all(),
        view_name='student_character_detail')

    class Meta:
        model = StudentCharacterTag
        fields = ['pk', 'url',
                  'name', 'states_count', 'student_characters']
