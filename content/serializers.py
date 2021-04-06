from rest_framework import serializers
from rest_framework.reverse import reverse

from content.models import Radical, Character, Word, WordSet, \
    DefinitionInWord, Sentence, DefinitionInCharacter, AudioFile


RELATED_MAX_NUM = 3


class RadicalSerializer(serializers.HyperlinkedModelSerializer):
    audio_url = serializers.ReadOnlyField()

    class Meta:
        model = Radical
        exclude = ['audio']


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
    radicals = serializers.SerializerMethodField()
    audio_url = serializers.ReadOnlyField()

    def get_radicals(self, character):
        radicals = character.radicals.order_by('radicalincharacter')
        l = [reverse('radical-detail',
                     kwargs={'pk': radical.pk},
                     request=self.context['request'])
             for radical in radicals]
        return l

    class Meta:
        model = Character
        exclude = ['note', 'archive', 'audio']


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
    characters = serializers.SerializerMethodField()
    audio_url = serializers.ReadOnlyField()

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
        exclude = ['note', 'archive', 'audio']


class WordSetSerializer(serializers.HyperlinkedModelSerializer):
    # TODO overwrite characters order when needed
    class Meta:
        model = WordSet
        fields = '__all__'
