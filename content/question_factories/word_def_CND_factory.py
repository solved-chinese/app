import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from content.models import Word, LinkedField, CNDQuestion
from .question_factory_registry import QuestionFactoryRegistry
from content.question_factories.constants import CannotAutoGenerate, \
    TOTAL_CND_OPTIONS, MAX_RANDOM_CHOICE_NUM
from content.utils import validate_chinese_character_or_x


logger = logging.getLogger(__name__)


@QuestionFactoryRegistry.register
class WordDefCNDFactory:
    question_type = "WordDefCND"
    question_model = Word

    @classmethod
    def generate(cls, ro):
        """
        incorrect answers should have the same number of question
        """
        word = ro.word
        assert word is not None

        old_question = CNDQuestion.objects.filter(
            question_type=cls.question_type,
            reviewable=ro,
        ).first()
        if old_question is not None:
            try:
                raise CannotAutoGenerate(f'the same question already generated '
                    f'(Q{old_question.general_question.pk})')
            except ObjectDoesNotExist:
                logger.warning("caught orphan CND, delete and regenerate")
                old_question.delete()

        if not word.primary_definition:
            raise CannotAutoGenerate('this word has no primary definition')

        if len(word.chinese) == 1:
            raise CannotAutoGenerate("Doesn't make sense for single char word")

        try:
            validate_chinese_character_or_x(word.chinese)
        except ValidationError:
            raise CannotAutoGenerate('This word contains wierd characters ')

        CND = CNDQuestion.objects.create(
            reviewable=ro,
            question_type=cls.question_type,
            question="How do you spell the word below",
            description="Drag the correct characters into the right order",
            title_link=LinkedField.of(word, 'primary_definition'),
            correct_answers=list(word.chinese),
            wrong_answers=[],
        )
        return CND.get_general_question()
