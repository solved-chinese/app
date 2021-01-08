from rest_framework import serializers

from content.models import Radical, Character, Word, WordSet, \
    DefinitionInWord, Sentence, DefinitionInCharacter


RELATED_MAX_NUM = 3


class RadicalSerializer(serializers.HyperlinkedModelSerializer):
    related_characters = serializers.SerializerMethodField()

    def get_related_characters(self, radical):
        """ TODO temporary """
        characters = radical.characters.all()[:RELATED_MAX_NUM]
        return SimpleCharacterSerializer(list(characters), many=True).data

    class Meta:
        model = Radical
        fields = '__all__'


class DefinitionInCharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInCharacter
        fields = ['definition']


class SimpleCharacterSerializer(serializers.ModelSerializer):
    full_definition = serializers.ReadOnlyField()

    class Meta:
        model = Character
        fields = ['chinese', 'pinyin', 'full_definition']


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInCharacterSerializer(many=True, read_only=True)
    related_words = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    def get_audio(self, obj):
        return "https://solvedchinese.org/media/audio/%E6%8B%BC[=h%C7%8Eo].mp3"

    def get_related_words(self, character):
        """ TODO temporary """
        words = character.words.all()[:RELATED_MAX_NUM]
        return SimpleWordSerializer(list(words), many=True).data

    class Meta:
        model = Character
        exclude = ['note', 'archive']


class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sentence
        fields = ['pinyin', 'chinese', 'translation']


class SimpleWordSerializer(serializers.ModelSerializer):
    full_definition = serializers.ReadOnlyField()

    class Meta:
        model = Word
        fields = ['chinese', 'pinyin', 'full_definition']


class DefinitionInWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInWord
        fields = ['part_of_speech', 'definition']


class WordSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInWordSerializer(
        many=True, read_only=True)
    sentences = SentenceSerializer(
        many=True, read_only=True)
    audio = serializers.SerializerMethodField()

    def get_audio(self, obj):
        return "https://solvedchinese.org/media/audio/%E6%8B%BC[=h%C7%8Eo].mp3"

    class Meta:
        model = Word
        exclude = ['note', 'archive']


class WordSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordSet
        fields = '__all__'
