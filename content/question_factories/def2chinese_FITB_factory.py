import logging

from django.core.exceptions import ObjectDoesNotExist

from content.models import Word, LinkedField, FITBQuestion
from .question_factory_registry import QuestionFactoryRegistry
from content.question_factories.constants import CannotAutoGenerate


logger = logging.getLogger(__name__)


@QuestionFactoryRegistry.register
class Def2ChineseFITBFactory:
    question_type = "Def2ChineseFITB"
    question_model = Word

    @classmethod
    def generate(cls, ro):
        """
        incorrect answers should have the same number of question
        """
        word = ro.word
        assert word is not None

        old_question = FITBQuestion.objects.filter(
            question_type=cls.question_type,
            reviewable=ro,
        ).first()
        if old_question is not None:
            try:
                raise CannotAutoGenerate(f'the same question already generated '
                    f'(Q{old_question.general_question.pk})')
            except ObjectDoesNotExist:
                logger.warning("caught orphan MC, delete and regenerate")
                old_question.delete()

        if not word.primary_definition:
            raise CannotAutoGenerate('this word has no primary definition')

        context_link = LinkedField.of(word, 'primary_sentence_chinese')
        title_link = LinkedField.of(word, 'primary_definition')
        answer_link = LinkedField.of(word, 'chinese')

        MC = FITBQuestion.objects.create(
            reviewable=ro,
            question_type=cls.question_type,
            context_link=context_link,
            question=f"Please type the chinese for",
            title_link=title_link,
            answer_link=answer_link,
        )

        return MC.get_general_question()
