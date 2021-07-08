from rest_framework import serializers
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_field, inline_serializer
from drf_spectacular.openapi import OpenApiTypes

from content.models import Radical, Character, Word, WordSet, \
    DefinitionInWord, Sentence, DefinitionInCharacter
from jiezi.rest.serializers import OrderedManyRelatedField


RELATED_MAX_NUM = 10


class RadicalSerializer(serializers.HyperlinkedModelSerializer):
    audio_url = serializers.ReadOnlyField()

    class Meta:
        model = Radical
        fields = ['url', 'pk', 'chinese', 'image', 'pinyin', 'definition',
                  'explanation', 'audio_url']


class DefinitionInCharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInCharacter
        fields = ['definition']


class SimpleCharacterSerializer(serializers.ModelSerializer):
    full_definition = serializers.ReadOnlyField()

    class Meta:
        model = Character
        fields = ['chinese', 'pinyin', 'full_definition', 'url', 'pk']


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInCharacterSerializer(many=True, read_only=True)
    radicals = OrderedManyRelatedField(
        child_relation=serializers.HyperlinkedRelatedField,
        order_by='radicalincharacter', read_only=True, view_name='radical-detail'
    )
    audio_url = serializers.ReadOnlyField()

    class Meta:
        model = Character
        fields = ['url', 'pk', 'definitions', 'radicals', 'audio_url',
                  'chinese', 'pinyin', 'character_type', 'memory_aid']


class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    audio_url = serializers.ReadOnlyField()

    class Meta:
        model = Sentence
        fields = ['pinyin_highlight', 'chinese_highlight',
                  'translation_highlight', 'audio_url']


class SimpleWordSerializer(serializers.ModelSerializer):
    full_definition = serializers.ReadOnlyField()

    class Meta:
        model = Word
        fields = ['chinese', 'pinyin', 'full_definition', 'url', 'pk']


class DefinitionInWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionInWord
        fields = ['part_of_speech', 'definition']


class WordSerializer(serializers.HyperlinkedModelSerializer):
    definitions = DefinitionInWordSerializer(
        many=True, read_only=True)
    sentences = SentenceSerializer(
        many=True, read_only=True)
    characters = serializers.SerializerMethodField()
    audio_url = serializers.ReadOnlyField()

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_characters(self, word):
        characters = word.characters.order_by('characterinword')
        # for single char word, give a list of a length 1, containing radical
        # urls separated by semicolon.
        if characters.count() == 1:
            l = [';'.join(
                 reverse('radical-detail',
                         kwargs={'pk': radical.pk},
                         request=self.context['request'])
                 for radical in characters.first()
                     .radicals.order_by('radicalincharacter'))]
        else:
            l = [reverse('character-detail',
                         kwargs={'pk': character.pk},
                         request=self.context['request'])
                 for character in characters]
        return l

    class Meta:
        model = Word
        fields = ['pk', 'url', 'definitions', 'sentences', 'characters',
                  'audio_url', 'chinese', 'pinyin', 'memory_aid']


class WordSetSerializer(serializers.HyperlinkedModelSerializer):
    words = SimpleWordSerializer(many=True, read_only=True)

    class Meta:
        model = WordSet
        exclude = ['note', 'archive']


class SimpleWordSetSerializer(serializers.ModelSerializer):
    # TODO overwrite characters order when needed
    class Meta:
        model = WordSet
        fields = ['pk', 'url', 'name', 'parent']
