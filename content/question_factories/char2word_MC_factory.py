import logging
from django.db.models import Count, Q

from content.models import Character, Word
from .question_factory_registry import QuestionFactoryRegistry
from .general_factory import GeneralFactory, MCFactoryMixin, WordFactoryMixin
from content.models.questions import LinkedField
from .constants import MAX_MC_CHOICE_NUM, MIN_MC_CHOICE_NUM, CannotAutoGenerate


@QuestionFactoryRegistry.register
class Char2WordMCFactory(MCFactoryMixin,
                         GeneralFactory):
    question_type = "Char2WordMC"
    question_model = Character
    question_order = 100
    logger = logging.getLogger(__name__)

    def generate_question_title(self, ro):
        return f'Which of the following characters can make a word with ' \
               f'"{ro.character.chinese}"?'

    def generate_correct_answer(self, ro):
        char = ro.character
        # extract from 2-char words that contains the current char
        word = Word.objects.annotate(
            char_count=Count('characters')
        ).filter(
            chinese__regex=r'^..$', characters__id=char.id,
            char_count=2, IC_level__isnull=False
        ).first()
        if not word:
            raise CannotAutoGenerate('no matching word')
        self.correct_word = word
        self.correct_char = word.characters.exclude(id=char.id).get()
        return LinkedField.of(self.correct_char, 'chinese')

    def generate_wrong_answer(self, ro):
        # 你好 with char = 你, correct_char = 好
        # qs1: 你们 => 我们 => 我, qs2: 很好 => 很
        char = ro.character
        def _validate_wrong_answer(wrong_answer):
            return (
                wrong_answer.chinese not in (self.correct_char.chinese,
                                             char.chinese)
                and not Word.objects.filter(
                    Q(chinese__contains=f"{char.chinese}{wrong_answer.chinese}")
                    | Q(chinese__contains=f"{wrong_answer.chinese}{char.chinese}")
                ).exists()
            )
        words = Word.objects.filter(chinese__regex=r'^..$')
        correct_word_related = words.filter(
            characters__in=self.correct_word.characters.all()
        )
        qs1 = Character.objects.filter(word__in=correct_word_related)
        correct_char_related = Word.objects.filter(
            characters__id=self.correct_char.id
        )
        qs2 = Character.objects.filter(word__in=correct_char_related)
        answer_list = self.extract_from_qs(
            [qs1,
             qs2,
             Character.objects.filter(is_done=True)],
            char,
            MIN_MC_CHOICE_NUM,
            MAX_MC_CHOICE_NUM,
            validate=_validate_wrong_answer,
        )
        return [LinkedField.of(obj, 'chinese') for obj in answer_list]

