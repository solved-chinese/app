import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from content.models import Word, LinkedField, CNDQuestion, Character, \
    MCQuestion, MCChoice, FITBQuestion
from content.utils import validate_chinese_character_or_brackets
from .constants import *


class GeneralFactory:
    logger = logging.getLogger(__name__)  # overwrite me
    question_model = None  # the content model tested by this question
    question_order = None # the order of question in this reviewable, auto gen
    # questions should use multiples of 10
    question_type = None  # a unique string representing question type
    question_form = None  # concrete question model MC/FITB/CND

    def clean_duplicate(self, ro):
        old_question = self.question_form.objects.filter(
            question_type=self.question_type,
            reviewable=ro,
        ).first()
        if old_question is not None:
            try:
                raise CannotAutoGenerate(f'the same question already generated '
                                         f'(Q{old_question.general_question.pk})')
            except ObjectDoesNotExist:
                self.logger.warning("caught orphan CND, delete and regenerate")
                old_question.delete()

    def clean(self, ro):
        if not isinstance(ro.concrete_object, self.question_model):
            raise ValueError(f"{ro} incompatible with required "
                             f"model {self.question_model}")

    def generate(self, ro):
        self.clean_duplicate(ro)
        self.clean(ro)
        self.correct_answer = self.generate_correct_answer(ro)
        self.wrong_answer = self.generate_wrong_answer(ro)
        concrete_question = self._generate(ro,
                                           self.correct_answer,
                                           self.wrong_answer)
        return concrete_question.get_general_question(order=self.question_order)

    def generate_context_link(self, ro):
        return None

    def extract_from_qs(self, querysets, correct_obj, min_num, max_num,
                        validate=None):
        """
        performs extraction of objects from querysets with
        returns:
            list of model objects
        """
        results = set()
        for queryset in querysets:
            if isinstance(correct_obj, queryset.model):
                queryset = queryset.exclude(id=correct_obj.id)
            queryset = queryset.exclude(IC_level__isnull=True).distinct()
            correct_IC_level = correct_obj.IC_level or 0
            before_qs = queryset.filter(
                IC_level__lte=correct_IC_level
            ).order_by('-IC_level')[:max_num]
            after_qs = queryset.filter(IC_level__gt=correct_IC_level)[:max_num]
            for obj in [*before_qs, *after_qs]:
                if validate is not None and not validate(obj):
                    continue
                results.add(obj)
                if len(results) == max_num:
                    return list(results)
            if len(results) >= min_num:
                return list(results)
        raise ValueError("there isn't enough qs to reach min_num")

    def generate_correct_answer(self, ro):
        return None

    def generate_wrong_answer(self, ro):
        return None


class MCFactoryMixin:
    question_form = MCQuestion

    def _generate(self, ro, correct_answer, wrong_answer):
        """
        args:
            correct_answer: LinkedField object
            wrong_answer: list of LinkedField objs
        """
        MC = MCQuestion.objects.create(
            reviewable=ro,
            question_type=self.question_type,
            context_link=self.generate_context_link(ro),
            question=self.generate_question_title(ro),
        )
        for answer in [correct_answer, *wrong_answer]:
            MCChoice.objects.create(
                linked_value=answer,
                weight=MCChoice.WeightType.CORRECT
                    if answer == correct_answer
                    else MCChoice.WeightType.AUTO_COMMON_WRONG,
                question=MC
            )
        return MC


class FITBFactoryMixin:
    question_form = FITBQuestion

    def _generate(self, ro, correct_answer, wrong_answer):
        # TODO remove hardcode
        title_link = LinkedField.of(ro.word, 'primary_definition')
        answer_link = LinkedField.of(ro.word, 'chinese')

        FITB = FITBQuestion.objects.create(
            reviewable=ro,
            question_type=self.question_type,
            context_link=self.generate_context_link(ro),
            question=f"Please type the chinese for",
            title_link=title_link,
            answer_link=answer_link,
        )
        return FITB


class CNDFactoryMixin:
    question_form = CNDQuestion

    def _generate(self, ro, correct_answer, wrong_answer):
        """
        args:
            correct_answer: list of str
            wrong_answer: list of str
        """
        # TODO remove hardcode
        CND = CNDQuestion.objects.create(
            reviewable=ro,
            question_type=self.question_type,
            question="How do you spell the word below",
            description="Click the correct characters into the right order",
            title_link=LinkedField.of(ro.word, 'primary_definition'),
            correct_answers=correct_answer,
            wrong_answers=wrong_answer,
        )
        return CND


class WordFactoryMixin:
    question_model = Word
    context_field = None  # used by default get_context_field

    def generate_related_words(self, word):
        word_len = len(word.chinese)
        # words that share a character with itself
        words = Word.objects.filter(
            characters__in=word.characters.all(),
        )
        # for single-char words, generate other single-char words that share
        # a character with itself
        if word_len == 1:
            words = words.filter(chinese__regex=r'^.{2,3}$')
            chars = Character.objects.filter(word__in=words)
            words = Word.objects.filter(
                chinese__regex=r'^.$', characters__in=chars
            ).exclude(chinese=word.chinese)
        elif word_len <= 3:
            words = words.filter(chinese__regex=r'^.{2}$')
        return words

    def generate_same_level_words(self, word):
        return Word.objects.filter(is_done=True,
                                   IC_level=word.IC_level)

    def generate_context_link(self, ro):
        if self.context_field:
            return LinkedField.of(ro.word, self.context_field)
        return None

    def generate_dummy_words(self):
        return Word.objects.filter(is_done=True)
