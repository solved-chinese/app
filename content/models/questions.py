import logging
import numpy as np

from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse


logger = logging.getLogger(__name__)


class GeneralQuestion(models.Model):
    reviewable = models.ForeignKey('ReviewableObject',
                                   on_delete=models.CASCADE,
                                   related_name='questions')
    MC = models.OneToOneField('MCQuestion', blank=True, null=True,
                              on_delete=models.CASCADE,
                              related_name='general_question')
    FITB = models.OneToOneField('FITBQuestion', blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='general_question')
    CND = models.OneToOneField('CNDQuestion', blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='general_question')

    def clean(self):
        """ make sure there is only one concrete review question """
        super().clean()
        i = iter([self.MC, self.FITB, self.CND])
        if not any(i) or any(i):
            raise ValidationError(
                f"MC {self.MC} FITB {self.FITB} CND {self.CND} "
                f"not only one exists")
        if self.reviewable != self.concrete_question.reviewable:
            raise ValidationError("self reviewable not same as concrete "
                                  "question reviewable")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def concrete_question(self):
        return self.MC or self.FITB or self.CND

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<Q{self.id}:{self.concrete_question}>"

    def __getattr__(self, item):
        """ redirects requests to concrete question """
        return getattr(self.concrete_question, item)


class BaseConcreteQuestion(models.Model):
    class ContextOption(models.TextChoices):
        NOT_SHOW = 'NOT', 'Not show'
        MUST_SHOW = 'MUST', 'Must show'
        AUTO = 'AUTO', 'Auto'

    question_form = None
    reviewable = models.ForeignKey('ReviewableObject',
                                   on_delete=models.CASCADE,
                                   related_name='+')
    question_type = models.CharField(
        max_length=20, blank=True, default="custom")
    context_link = models.ForeignKey('LinkedField',
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)
    context_option = models.CharField(max_length=4,
                                      choices=ContextOption.choices,
                                      default=ContextOption.AUTO)
    question = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def render(self):
        client_dict = {
            'question': _handle_text_with_audio(self.question),
        }
        context = self.context
        if self.context_option == self.ContextOption.MUST_SHOW:
            if not context:
                raise ValueError("must show context but no context found")
        elif self.context_option == self.ContextOption.NOT_SHOW:
            context = None
        if context:
            client_dict['context'] = _handle_text_with_audio(context)
        server_dict = {
            'give_context': bool(context),
        }
        return client_dict, server_dict

    @property
    def context(self):
        if self.context_link is None:
            return None
        return self.context_link.value

    def get_general_question(self):
        try:
            return self.general_question
        except ObjectDoesNotExist:
            kwargs = {
                'reviewable': self.reviewable,
                self.question_form: self
            }
            return GeneralQuestion.objects.create(**kwargs)

    def get_admin_url(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return reverse(f'admin:{app}_{model}_change', args=(self.id,))

    def check_answer(self, request_dict, server_dict):
        """
        returns response_dict, is_correct
        However, be prepared to handle client error
        """
        if 'answer' not in request_dict:
            raise serializers.ValidationError('"answer" not found in request')
        client_answer = request_dict['answer']
        server_answer = server_dict['answer']
        if client_answer is None:
            is_correct = False
        else:
            if isinstance(server_answer, int):
                client_answer = int(client_answer)
            is_correct = client_answer == server_dict['answer']
        response_dict = {
            'is_correct': is_correct,
            'answer': server_answer,
        }
        return response_dict, is_correct

    def get_absolute_url(self):
        return f"/learning/review/?qid={self.get_general_question().pk}"

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<{self.question_form}{self.id}: " \
               f"{self.question_type} on {self.reviewable}>"


class LinkedField(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=50, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    overwrite = models.CharField(max_length=200, blank=True)

    @property
    def value(self):
        if self.overwrite:
            return self.overwrite
        value = getattr(self.content_object, self.field_name)
        if not value:
            raise ValidationError("value None")
        return value

    def clean(self):
        if self.overwrite and self.object_id:
            raise ValidationError("can't have overwrite and object both exist")
        if not self.overwrite and not self.object_id:
            raise ValidationError("can't have overwrite and object both blank")

    @classmethod
    def of(cls, object, field_name):
        content_type = ContentType.objects.get_for_model(object)
        object_id = object.id
        return cls.objects.get_or_create(content_type=content_type,
                                         object_id=object_id,
                                         field_name=field_name)[0]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.overwrite:
            return f"<overwritten: {self.overwrite}>"
        return f"<{repr(self.content_object)}'s {self.field_name}>"


class MCChoice(models.Model):
    class WeightType(models.IntegerChoices):
        CORRECT = 0
        AUTO_COMMON_WRONG = 100
        COMMON_WRONG = 101
        MISSLEADING = 500
        VERY_MISSLEADING = 2000

    linked_value = models.ForeignKey(LinkedField,
                                     on_delete=models.CASCADE,
                                     related_name='+')
    weight = models.PositiveSmallIntegerField(choices=WeightType.choices)
    question = models.ForeignKey('MCQuestion', on_delete=models.CASCADE,
                                 related_name='choices',
                                 related_query_name='choice')

    class Meta:
        ordering = ['weight']

    @property
    def value(self):
        return self.linked_value.value


class MCQuestion(BaseConcreteQuestion):
    question_form = 'MC'
    num_choices = models.PositiveSmallIntegerField(default=4)

    def render(self):
        weights = np.array(self.choices.values_list('weight', flat=True))
        total_cnt = len(weights)
        if total_cnt < self.num_choices:
            raise ValidationError(f"there are {total_cnt} choices, "
                                  f"fewer than {self.num_choices}")

        answer_cnt = total_cnt - np.count_nonzero(weights)
        if answer_cnt != 1:
            raise ValidationError(f"there are {answer_cnt} correct answers, "
                                  f"not one")

        choice_indexes = np.random.choice(np.arange(total_cnt),
                                          size=self.num_choices - 1,
                                          replace=False,
                                          p=weights / np.sum(weights)
                                          ).tolist()
        answer = np.random.randint(self.num_choices)
        choice_indexes.insert(answer, 0)

        choice_list = list(self.choices.all())
        choices = [choice_list[i].value for i in choice_indexes]
        choice_pks = [choice_list[i].pk for i in choice_indexes]

        client_dict, server_dict = super().render()
        client_dict.update({
            'choices': [_handle_text_with_audio(choice) for choice in choices]
        })
        server_dict.update({
            'choice_pks': choice_pks,
            'answer': answer,
        })
        return client_dict, server_dict


class FITBQuestion(BaseConcreteQuestion):
    question_form = 'FITB'
    title_link = models.ForeignKey(LinkedField,
                                   on_delete=models.CASCADE,
                                   related_name='+')
    answer_link = models.ForeignKey(LinkedField,
                                    on_delete=models.CASCADE,
                                    related_name='+')

    def render(self):
        title = self.title_link.value
        answer = self.answer_link.value
        if not answer or not title:
            raise ValidationError("answer or extra_information None")
        client_dict, server_dict = super().render()
        client_dict.update({
            'title': _handle_text_with_audio(title),
        })
        server_dict.update({
            'answer': answer,
        })
        return client_dict, server_dict


    def get_absolute_url(self):
        return f"/content/question/{self.get_general_question().pk}"


class CNDQuestion(BaseConcreteQuestion):
    question_form = 'CND'
    description = models.TextField(max_length=200, blank=True)
    title_link = models.ForeignKey(LinkedField,
                                   on_delete=models.CASCADE,
                                   related_name='+')
    correct_answers = ArrayField(models.CharField(max_length=5))
    wrong_answers = ArrayField(models.CharField(max_length=5))

    def render(self):
        title = self.title_link.value
        if not self.correct_answers:
            raise ValidationError("no correct_answers")
        choices = self.correct_answers.copy()
        choices.extend(self.wrong_answers)
        np.random.shuffle(choices)
        client_dict, server_dict = super().render()
        client_dict.update({
            'title': _handle_text_with_audio(title),
            'description': self.description,
            'answer_length': len(self.correct_answers),
            'choices': choices
        })
        server_dict.update({
            'answer': self.correct_answers,
        })
        return client_dict, server_dict

    def get_absolute_url(self):
        return f"/content/question/{self.get_general_question().pk}"


def _handle_text_with_audio(obj):
    assert isinstance(obj, str)
    return {"text": obj,
            "audio": "https://solvedchinese.org/media/audio/%E6%8B%BC[=h%C7%8Eo].mp3"}