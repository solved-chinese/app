from rest_framework import serializers
from content.serializers import CharacterSerializer
from learning.models import StudentCharacter, StudentCharacterTag


class StudentCharacterSimpleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='student_character_detail')
    chinese = serializers.SerializerMethodField()

    def get_chinese(self, obj):
        return obj.character.chinese

    class Meta:
        model = StudentCharacter
        fields = ['pk', 'url',
                  'chinese']


class StudentCharacterSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = StudentCharacter
        fields = ['pk',
                  'character',
                  'learned', 'mastered']


class SimpleStudentCharacterTagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='student_character_tag_detail')
    learned_cnt = serializers.SerializerMethodField()
    mastered_cnt = serializers.SerializerMethodField()
    total_cnt = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentCharacterTag
        fields = ['pk', 'url',
                  'name', 'learned_cnt', 'mastered_cnt', 'total_cnt']

    def get_learned_cnt(self, obj):
        return obj.user_characters.filter(learned=True).count()

    def get_mastered_cnt(self, obj):
        return obj.user_characters.filter(mastered=True).count()

    def get_total_cnt(self, obj):
        return obj.user_characters.count()

    def get_name(self, obj):
        return obj.character_set.name


class StudentCharacterTagSerializer(SimpleStudentCharacterTagSerializer):
    student_characters = serializers.HyperlinkedRelatedField(
        many=True, queryset=StudentCharacter.objects.all(),
        view_name='student_character_detail')

    class Meta:
        model = StudentCharacterTag
        fields = ['pk', 'url',
                  'name', 'learned_cnt', 'mastered_cnt', 'total_cnt',
                  'student_characters']