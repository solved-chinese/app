import logging

from content.models import Character
from .question_factory_registry import QuestionFactoryRegistry
from .general_factory import GeneralFactory, CNDFactoryMixin, WordFactoryMixin
from .constants import MIN_CND_OPTIONS, MAX_CND_OPTIONS, CannotAutoGenerate


@QuestionFactoryRegistry.register
class WordDefCNDFactory(WordFactoryMixin,
                        CNDFactoryMixin,
                        GeneralFactory):
    question_type = "WordDefCND"
    question_order = 30
    logger = logging.getLogger(__name__)

    def clean(self, ro):
        super().clean(ro)
        if len(ro.word.chinese) == 1:
            raise CannotAutoGenerate("meaningless for single char word")

    def generate_correct_answer(self, ro):
        chinese = ro.word.chinese
        answer = list(chinese)
        left_index = chinese.find('(')
        if left_index != -1:
            assert chinese[left_index + 2] == ')', \
                'left right bracket not match'
            chinese.replace('(', '')
            chinese.replace(')', '')
            answer[left_index] = f"({answer[left_index]})"
        return answer

    def generate_wrong_answer(self, ro):
        min_num = MIN_CND_OPTIONS - len(self.correct_answer)
        max_num = MAX_CND_OPTIONS - len(self.correct_answer)
        answer_list = self.extract_from_qs(
            [self.generate_related_words(ro.word),
             self.generate_same_level_words(ro.word),
             self.generate_dummy_words()],
            ro.word,
            min_num,
            max_num
        )
        return [c.chinese for c in answer_list]

    def extract_from_qs(self, querysets, obj, min_num, max_num):
        new_querysets = []
        for queryset in querysets:
            queryset = Character.objects.filter(
                word__in=queryset.all()
            ).exclude(
                id__in=obj.characters.all()
            )
            new_querysets.append(queryset)
        return super().extract_from_qs(new_querysets, obj, min_num, max_num)
