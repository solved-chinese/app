import logging

from django.core.exceptions import ObjectDoesNotExist

from content.models import Word, LinkedField, MCQuestion, MCChoice, GeneralQuestion
from .question_factory_registry import QuestionFactoryRegistry
from content.question_factories.constants import CannotAutoGenerate, \
    MAX_RANDOM_CHOICE_NUM, MAX_MC_CHOICE_NUM, MIN_MC_CHOICE_NUM


logger = logging.getLogger(__name__)


@QuestionFactoryRegistry.register
class Chinese2DefMCFactory:
    question_type = "Chinese2DefMC"
    question_model = Word

    @classmethod
    def generate(cls, ro):
        """
        incorrect answers should have the same number of question
        """
        word = ro.word
        assert word is not None

        old_question = MCQuestion.objects.filter(
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

        related_character_queryset = Word.objects.filter(
            characters__in=word.characters.all())[:MAX_RANDOM_CHOICE_NUM]
        same_set_queryset = Word.objects.filter(
            word_set__in=word.word_sets.all())[:MAX_RANDOM_CHOICE_NUM]
        qs = related_character_queryset | same_set_queryset
        qs = qs.exclude(pk=word.pk).distinct()

        # select [MIN_MC_CHOICE_NUM, MAX_MC_CHOICE_NUM] wrong answers
        qs = qs.order_by('?')
        candidate_words = []
        for candidate_word in qs.all():
            if candidate_word.primary_definition:
                candidate_words.append(candidate_word)
            if len(candidate_words) >= MAX_MC_CHOICE_NUM:
                break
        if len(candidate_words) < MIN_MC_CHOICE_NUM:
            raise CannotAutoGenerate("there are too few wrong options")

        context_link = LinkedField.of(word, 'primary_sentence_chinese')
        MC = MCQuestion.objects.create(
            reviewable=ro,
            question_type=cls.question_type,
            context_link=context_link,
            question=f"What does {word.chinese} mean?",
        )

        candidate_words.append(word)
        for candidate_word in candidate_words:
            linked_value = LinkedField.of(candidate_word, 'primary_definition')
            MCChoice.objects.create(
                linked_value=linked_value,
                weight=MCChoice.WeightType.CORRECT
                    if candidate_word == word
                    else MCChoice.WeightType.AUTO_COMMON_WRONG,
                question=MC
            )
        return MC.get_general_question()
