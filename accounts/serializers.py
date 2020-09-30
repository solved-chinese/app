from rest_framework import serializers
from .models import User, UserCharacterTag, UserCharacter
from learning.serializers import CharacterSerializer


class UserCharacterSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = UserCharacter
        fields = ['pk',
                  'character',
                  'learned', 'mastered']


class SimpleUserCharacterTagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user_character_tag_detail')
    learned_cnt = serializers.SerializerMethodField()
    mastered_cnt = serializers.SerializerMethodField()
    total_cnt = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserCharacterTag
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


class UserCharacterTagSerializer(SimpleUserCharacterTagSerializer):
    user_characters = serializers.HyperlinkedRelatedField(many=True,
        queryset=UserCharacter.objects.all(),
        view_name='user_character_detail')

    class Meta:
        model = UserCharacterTag
        fields = ['pk', 'url',
                  'name', 'learned_cnt', 'mastered_cnt', 'total_cnt',
                  'user_characters']


class UserSerializer(serializers.ModelSerializer):
    user_characters = serializers.HyperlinkedRelatedField(many=True,
        queryset=UserCharacter.objects.all(),
        view_name='user_character_detail')
    user_character_tags = SimpleUserCharacterTagSerializer(read_only=True,
                                                           many=True)

    class Meta:
        model = User
        fields = ['pk',
                  'username',
                  'user_characters', 'user_character_tags']
