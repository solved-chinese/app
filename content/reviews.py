import random

from django.db import models

from .models import Character
from .audio import generate_audio_tag


MAX_RANDOM_CHOICES = 20


class ReviewQuestion:
    test_field = None
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
    def get_queryset(cls, character, characters=None):
        if characters is None:
            characters = Character.objects.all()
        kwargs = {f"{cls.choice_field}__unaccent":
                      getattr(character, cls.choice_field)}
        return characters.exclude(**kwargs)

    @classmethod
    def get_question(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def generate_question(cls, character, characters=None):
        queryset = cls.get_queryset(character, characters)
        queryset = queryset[:MAX_RANDOM_CHOICES]
        choices = [getattr(c, cls.choice_field)
                   for c in random.sample(list(queryset), cls.num_choices - 1)]
        ans_index = random.randint(0, cls.num_choices - 1)
        choices.insert(ans_index, getattr(character, cls.choice_field))
        return ans_index, {'question': cls.get_question(character),
                           'choices': choices}


class DefinitionMCAnswerField(MultipleChoice):
    test_field = 'definition_1'
    choice_field = 'definition_1'

    @classmethod
    def get_question(cls, character):
        return f"What is the definition of {character.chinese}?"


class DefinitionMCAnswerCharacter(MultipleChoice):
    test_field = 'definition_1'
    choice_field = 'chinese'

    @classmethod
    def get_question(cls, character):
        return f'Which of the following characters means ' \
               f'"{character.definition_1}"?'


class PinyinMC(MultipleChoice):
    test_field = 'pinyin'
    choice_field = 'chinese'

    @classmethod
    def get_question(cls, character):
        return f""" 
            Which of the following characters is pronounced 
            {character.pinyin} {generate_audio_tag(pinyin=character.pinyin)}? 
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
            queryset = cls.get_queryset(character, characters)
            queryset = queryset[:MAX_RANDOM_CHOICES]
            wrong_character = random.choice(queryset)
            field = getattr(wrong_character, cls.choice_field)
        return ans_index, {'question': cls.get_question(character, field),
                           'choices': ['True', 'False']}


class PinyinTOF(TrueOrFalse):
    test_field = 'pinyin'
    choice_field = 'pinyin'

    @classmethod
    def get_question(cls, character, field):
        return f"""
        The pronunciation of {character.chinese} is "{field}" 
        {generate_audio_tag(pinyin=field)}?
        """


class DefinitionTOF(TrueOrFalse):
    test_field = 'definition_1'
    choice_field = 'definition_1'

    @classmethod
    def get_question(cls, character, field):
        return f'The definition of {character.chinese} is "{field}"?'


class DefinitionFITB(ReviewQuestion):
    test_field = 'definition_1'
    template = 'content/reviews/fill_in_the_blank.html'

    @classmethod
    def generate_question(cls, character, characters=None):
        # randomly select from two examples if both exist
        example = character.get_example_2_sentence()
        if example is None or random.random() < 0.5:
            example = character.get_example_sentence()
        return character.chinese, \
               {'question': example.replace(character.chinese, '_')}


class PinyinFITB(ReviewQuestion):
    test_field = 'pinyin'
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
        word_blank = word.replace(character.chinese, '_')
        pinyin = pinyin.replace('+', '')
        return character.chinese, \
               {'question': f"""{word_blank} /{pinyin}/ 
                            {generate_audio_tag(chinese=word)}"""}


AVAILABLE_REVIEW_TYPES = [DefinitionMCAnswerField, DefinitionMCAnswerCharacter,
                          PinyinMC, DefinitionTOF, PinyinTOF,
                          DefinitionFITB, PinyinFITB]

def factory_review_manager():
    class AbstractModel(models.Model):
        class Meta:
            abstract = True
    _review_fields = {}
    for review_type in AVAILABLE_REVIEW_TYPES:
        AbstractModel.add_to_class(f"use_{review_type}",
                                   models.BooleanField(default=True))
    return AbstractModel

class ReviewManager(factory_review_manager()):
    def get_review_type(self, field_name):
        available_review_types = []
        for review_type in AVAILABLE_REVIEW_TYPES:
            if review_type.test_field == field_name \
                    and getattr(self, f"use_{review_type}"):
                available_review_types.append(review_type)
        assert available_review_types, \
            'There should be at least one review type available'
        return random.choice(available_review_types)

    @classmethod
    def get(cls, **kwargs):
        return cls.objects.get_or_create(**kwargs)[0]