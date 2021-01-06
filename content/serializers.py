from rest_framework import serializers

from content.models import Radical, Character, Word, WordSet, \
    DefinitionInWord, Sentence, DefinitionInCharacter


class RadicalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Radical
        fields = '__all__'


class DefinitionInCharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInCharacter
        fields = ['definition']



class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInCharacterSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = '__all__'


class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sentence
        fields = ['pinyin', 'chinese', 'translation']


class DefinitionInWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInWord
        fields = ['part_of_speech', 'definition']


class WordSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInWordSerializer(
        many=True, read_only=True)
    sentences = SentenceSerializer(
        many=True, read_only=True)

    class Meta:
        model = Word
        fields = '__all__'


class WordSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordSet
        fields = '__all__'
