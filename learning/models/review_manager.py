from django.core.exceptions import ValidationError
from django.db import models
from django import forms

from content.reviews import *
from learning.models import Ability
from jiezi.utils.mixins import CleanBeforeSaveMixin


def factory_review_manager():
    class AbstractModel(models.Model):
        class Meta:
            abstract = True
    for review_type in AVAILABLE_REVIEW_TYPES:
        AbstractModel.add_to_class(f"use_{review_type.__name__}",
                                   models.BooleanField(default=True))
    return AbstractModel


class ReviewManager(CleanBeforeSaveMixin, factory_review_manager()):
    TOLERANT_REVIEW_1_QUESTION = DefinitionMCAnswerField
    TOLERANT_REVIEW_2_QUESTION = PinyinMC
    monitored_abilities = models.ManyToManyField('learning.Ability',
                                                 related_name='+')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        codes = set()
        for review_type in AVAILABLE_REVIEW_TYPES:
            if getattr(self, f"use_{review_type.__name__}"):
                codes.update(review_type.test_abilities)
        codes = list(codes)
        abilities = list(Ability.objects.filter(code__in=codes))
        self.monitored_abilities.set(abilities)

    def get_review_type(self, ability_code):
        available_review_types = []
        for review_type in AVAILABLE_REVIEW_TYPES:
            if ability_code in review_type.test_abilities \
                    and getattr(self, f"use_{review_type.__name__}"):
                available_review_types.append(review_type)
        assert available_review_types, \
            'There should be at least one review type available'
        return random.choice(available_review_types)

    def clean(self):
        # at least there should be one review type available
        if not any(getattr(self, f"use_{review_type.__name__}")
                   for review_type in AVAILABLE_REVIEW_TYPES):
            raise ValidationError("There must be at least one review "
                                  "type selected",
                                  code='invalid')

    def to_get_kwargs(self, prefix_name=None):
        kwargs = {}
        for review_type in AVAILABLE_REVIEW_TYPES:
            attr_name = f"use_{review_type.__name__}"
            if prefix_name is None:
                kwargs_name = attr_name
            else:
                kwargs_name = f"{prefix_name}_{attr_name}"
            kwargs[kwargs_name] = getattr(self, attr_name)
        return kwargs

    def as_display_html(self):
        from ..fields import ReviewManagerWidget
        return ReviewManagerWidget().render(
            'review_manager',
            self.to_get_kwargs(),
            {'disabled': True}
        )

    @classmethod
    def get(cls, **kwargs):
        d = {}
        for review_type in AVAILABLE_REVIEW_TYPES:
            d[f"use_{review_type.__name__}"] = True
        d.update(kwargs)
        return cls.objects.get_or_create(**d)[0]

    @classmethod
    def get_default_pk(cls):
        return cls.get().pk
