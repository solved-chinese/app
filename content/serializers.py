from rest_framework import serializers

from content.models import Radical, Character, Word, WordSet, \
    DefinitionInWord, Sentence


class RadicalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Radical
        fields = '__all__'


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
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
