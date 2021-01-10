import logging
import numpy as np

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
    DRAG = models.OneToOneField('DRAGQuestion', blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='general_question')

    def clean(self):
        """ make sure there is only one concrete review question """
        super().clean()
        i = iter([self.MC, self.FITB, self.DRAG])
        if not any(i) or any(i):
            raise ValidationError(
                f"MC {self.MC} FITB {self.FITB} drag {self.DRAG} "
                f"not only one exists")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def concrete_question(self):
        return self.MC or self.FITB or self.DRAG

    def render(self, give_context=False):
        return self.concrete_question.render(give_context=give_context)

    def check_answer(self, request_dict, server_dict):
        return self.concrete_question.check_answer(request_dict, server_dict)


class BaseConcreteQuestion(models.Model):
    question_form = None

    context_link = models.OneToOneField('LinkedField',
                                        on_delete=models.SET_NULL,
                                        null=True, blank=True)
    must_show_context = models.BooleanField(default=False)
    question = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def render(self, give_context=False):
        client_dict = {
            'form': self.question_form,
            'question': self.question,
        }
        server_dict = {
            'give_context': give_context,
        }
        if give_context:
            context = self.context
            if not context:
                raise ValueError("give_context true but no context found")
            client_dict['context'] = context
        return client_dict, server_dict

    def check_answer(self, request_dict, server_dict):
        """ returns response_dict, is_correct """
        is_correct = request_dict['answer'] == server_dict['answer']
        response_dict = {
            'is_correct': is_correct,
            'answer': server_dict['answer'],
        }
        return response_dict, is_correct

    @property
    def context(self):
        if self.context_link is None:
            return None
        return self.context_link.value


class LinkedField(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=20, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    overwrite = models.CharField(max_length=200, blank=True)

    @property
    def value(self):
        if self.overwrite:
            return self.overwrite
        try:
            model = self.content_type.model_class()
            obj = model.objects.get(pk=self.object_id)
            return getattr(obj, self.field_name)
        except Exception as e:
            logger.warning("field value corrupt, self deletion", exc_info=True)
            self.delete()
        return None

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
            return f"<overwritten field>"
        model = self.content_type.model_class()
        obj = model.objects.get(pk=self.object_id)
        return f"<{repr(obj)}'s {self.field_name}>"


class MCChoice(models.Model):
    class WeightType(models.IntegerChoices):
        CORRECT = 0
        COMMON_WRONG = 100
        MISSLEADING = 500
        VERY_MISSLEADING = 2000

    linked_value = models.OneToOneField(LinkedField, on_delete=models.CASCADE)
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

    def render(self, give_context=False):
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

        client_dict, server_dict = super().render(give_context=give_context)
        client_dict.update({
            'choices': choices
        })
        server_dict.update({
            'choice_pks': choice_pks,
            'answer': answer,
        })
        return client_dict, server_dict


class FITBQuestion(BaseConcreteQuestion):
    question_form = 'FITB'
    pass


class DRAGQuestion(BaseConcreteQuestion):
    question_form = 'DRAG'
    pass