import random
import copy

from .models import Character
from .audio import generate_audio_tag
from learning.models.ability import Ability


MAX_RANDOM_CHOICES = 20


class ReviewQuestion:
    verbose_name = 'NOT DEFINED'
    test_abilities = ()
    template = None

    @classmethod
    def generate_question(cls, character, characters=None):
        """ returns (correct_answer, context) """
        raise NotImplementedError


class MultipleChoice(ReviewQuestion):
    template = 'content/reviews/multiple_choice.html'
    num_choices = 4
    choice_field = None

    @classmethod
    def get_queryset(cls, character, characters=None,
                     assert_as_least=0):
        if characters is None:
            characters = Character.objects.all()
        kwargs = {f"{cls.choice_field}__unaccent":
                      getattr(character, cls.choice_field)}
        queryset = characters.exclude(**kwargs)
        if queryset.count() < assert_as_least:
            queryset = Character.objects.all().exclude(**kwargs)
        return queryset

    @classmethod
    def get_question(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def generate_question(cls, character, characters=None):
        queryset = cls.get_queryset(character, characters,
                                    assert_as_least=cls.num_choices - 1)
        queryset = queryset[:MAX_RANDOM_CHOICES]
        wrong_answer_set = {getattr(c, cls.choice_field)
                            for c in queryset.all()}
        choices = random.sample(wrong_answer_set, cls.num_choices - 1)
        ans_index = random.randint(0, cls.num_choices - 1)
        choices.insert(ans_index, getattr(character, cls.choice_field))
        return ans_index, {'question': cls.get_question(character),
                           'choices': choices}


class DefinitionMCAnswerField(MultipleChoice):
    verbose_name = 'Definition Multiple Choice Meaning'
    test_abilities = (Ability.DEFINITION,)
    choice_field = 'definition_1'

    @classmethod
    def get_question(cls, character):
        return f"What is the definition of {character.chinese}?"


class DefinitionMCAnswerCharacter(MultipleChoice):
    verbose_name = 'Definition Multiple Choice Character'
    test_abilities = (Ability.DEFINITION,)
    choice_field = 'chinese'

    @classmethod
    def get_queryset(cls, character, characters=None,
                     assert_as_least=0):
        """
        ma and ne both mean question particle
        """
        if characters is None:
            characters = Character.objects.all()
        queryset = characters.exclude(definition_1=character.definition_1)
        if queryset.count() < assert_as_least:
            queryset = Character.objects.all().exclude(
                    definition_1=character.definition_1)
        return queryset

    @classmethod
    def get_question(cls, character):
        return f'Which of the following characters means ' \
               f'"{character.definition_1}"?'


class PinyinMC(MultipleChoice):
    verbose_name = 'Pinyin Multiple Choice'
    test_abilities = (Ability.PRONUNCIATION,)
    choice_field = 'chinese'

    @classmethod
    def get_question(cls, character):
        return f""" 
            Which of the following characters is pronounced 
            "{character.pinyin}" 
            {generate_audio_tag(pinyin=character.pinyin)}? 
        """


class TrueOrFalse(MultipleChoice):
    TRUE_PROB = 0.5

    @classmethod
    def get_question(cls, character, field):
        raise NotImplementedError

    @classmethod
    def generate_question(cls, character, characters=None):
        if random.random() < cls.TRUE_PROB:
            ans_index = 0
            field = getattr(character, cls.choice_field)
        else:
            ans_index = 1
            queryset = cls.get_queryset(character, characters,
                                        assert_as_least=1)
            queryset = queryset[:MAX_RANDOM_CHOICES]
            wrong_character = random.choice(queryset)
            field = getattr(wrong_character, cls.choice_field)
        return ans_index, {'question': cls.get_question(character, field),
                           'choices': ['True', 'False']}


class PinyinTOF(TrueOrFalse):
    verbose_name = 'Pinyin True or False'
    test_abilities = (Ability.PRONUNCIATION,)
    choice_field = 'pinyin'

    @classmethod
    def get_question(cls, character, field):
        return f"""
        Is "{character.chinese}" pronounced as "{field}" 
        {generate_audio_tag(pinyin=field)}?
        """


class DefinitionTOF(TrueOrFalse):
    verbose_name = 'Definition True or False'
    test_abilities = (Ability.DEFINITION,)
    choice_field = 'definition_1'

    @classmethod
    def get_question(cls, character, field):
        return f'Does "{character.chinese}" mean "{field}"?'


class DefinitionFITB(ReviewQuestion):
    verbose_name = 'Example Word fill-in-the-blank with Characters'
    test_abilities = (Ability.FORM, Ability.DEFINITION)
    template = 'content/reviews/fill_in_the_blank.html'

    @classmethod
    def generate_question(cls, character, characters=None):
        # randomly select from two examples if both exist
        example = character.get_example_2_sentence()
        if example is None or random.random() < 0.5:
            example = character.get_example_sentence()
        return character.chinese, \
               {'question': example.replace(character.chinese, '___').
                   replace('<br>', '')}


class PinyinFITB(ReviewQuestion):
    verbose_name = 'Example word fill-in-the-blank without Characters'
    test_abilities = (Ability.FORM, Ability.PRONUNCIATION)
    template = 'content/reviews/fill_in_the_blank.html'

    @classmethod
    def generate_question(cls, character, characters=None):
        # randomly select from two examples if both exist
        word = character.example_2_word
        pinyin = character.example_2_pinyin
        if not word or random.random() < 0.5:
            word = character.example_1_word
            pinyin = character.example_1_pinyin
        word = word.replace('+', '')
        word_blank = word.replace(character.chinese, '___').replace('<br>', '')
        pinyin = pinyin.replace('+', '')
        return character.chinese, \
               {'question': f"""{word_blank} /{pinyin}/ 
                            {generate_audio_tag(chinese=word)}"""}


AVAILABLE_REVIEW_TYPES = (DefinitionMCAnswerField, DefinitionMCAnswerCharacter,
                          PinyinMC, DefinitionTOF, PinyinTOF,
                          DefinitionFITB, PinyinFITB)
