import re
import itertools

from content.models import Character, Word, MCQuestion, MCChoice, \
    GeneralQuestion, LinkedField
from content.models.general_content_model import CHINESE_CHAR_REGEX
from .question_factory_registry import QuestionFactoryRegistry


class CannotAutomaticallyGenerateException(Exception):
    pass


MC_CHOICE_NUM = 10
MAX_RANDOM_CHOICE_NUM = 50


@QuestionFactoryRegistry.register()
class Chinese2PinyinMCFactory:
    question_type = "Chinese2Pinyin"
    question_model = Word

    @classmethod
    def generate(cls, ro):
        """
        incorrect answers should have the same number of chinese characters
        """
        word = ro.word
        assert word is not None
        len_chinese = len(re.findall(CHINESE_CHAR_REGEX, word.chinese))
        related_character_queryset = filter_num_chinese(
            Word.objects.filter(characters__in=word.characters.distinct()),
            len_chinese
        )[:MAX_RANDOM_CHOICE_NUM]
        same_word_set_queryset = filter_num_chinese(
            Word.objects.filter(word_set__in=word.word_sets.distinct()),
            len_chinese
        )[:MAX_RANDOM_CHOICE_NUM]
        queryset = related_character_queryset | same_word_set_queryset
        queryset = queryset.exclude(pk=word.pk).distinct[:MAX_RANDOM_CHOICE_NUM]
        if queryset.count() < MC_CHOICE_NUM:
            raise CannotAutomaticallyGenerateException(
                "Too few elements in queryset")
        queryset = queryset.order_by('?')[:MAX_RANDOM_CHOICE_NUM]
        reviwable = word.get_reviewable_object()
        MC = MCQuestion.objects.create(
            question_type=cls.question_type,
            question=f"Which of the following question means {word.chinese}",
        )
        for candidate_word in itertools.chain(queryset, [word]):
            linked_value = LinkedField.of(candidate_word, 'pinyin')
            MCChoice.objects.create(
                linked_value=linked_value,
                weight=MCChoice.WeightType.AUTO_COMMON_WRONG
                if candidate_word.pk == word.pk else MCChoice.WeightType.CORRECT,
                question=MC
            )
        return GeneralQuestion.objects.create(MC=MC, reviewable=reviwable)


def filter_num_chinese(qs, len_chinese):
    return qs.filter(
        chinese__regex=f"^{CHINESE_CHAR_REGEX}{{{len_chinese}}}$"
    ).exclude(
        chinese__regex=f"^{CHINESE_CHAR_REGEX}{{{len_chinese+1}}}$"
    )
