import logging

from django.core.exceptions import ObjectDoesNotExist

from content.models import Word, LinkedField, MCQuestion, MCChoice, GeneralQuestion
from .question_factory_registry import QuestionFactoryRegistry
from content.question_factories.constants import CannotAutoGenerate, \
    MAX_RANDOM_CHOICE_NUM, MAX_MC_CHOICE_NUM, MIN_MC_CHOICE_NUM
from .general_factory import GeneralFactory, MCFactoryMixin, WordFactoryMixin


@QuestionFactoryRegistry.register
class Chinese2DefMCFactory(WordFactoryMixin,
                          MCFactoryMixin,
                          GeneralFactory):
    question_type = "Chinese2DefMC"
    question_order = 20
    context_field = 'primary_sentence_chinese'
    logger = logging.getLogger(__name__)

    def generate_question_title(self, ro):
        return f"What does {ro.word.chinese} mean?"

    def generate_correct_answer(self, ro):
        return LinkedField.of(ro.word, 'primary_definition')

    def generate_wrong_answer(self, ro):
        answer_list = self.extract_from_qs(
            [self.generate_related_words(ro.word),
             self.generate_same_level_words(ro.word),
             self.generate_dummy_words()],
            ro.word,
            MIN_MC_CHOICE_NUM,
            MAX_MC_CHOICE_NUM,
        )
        return [LinkedField.of(answer, 'primary_definition')
                for answer in answer_list]

