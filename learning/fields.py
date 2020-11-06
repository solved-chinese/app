from django import forms
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.urls import reverse

from learning.models import ReviewManager
from content.models import Character
from content.reviews import AVAILABLE_REVIEW_TYPES
from .models import Ability


class ReviewManagerWidget(forms.Widget):
    template_name = 'learning/review_manager_widget.html'

    def get_context(self, name, value, attrs):
        """
        value should be either None or a dict (kwargs to ReviewManager.get)
        """
        assert value is None or isinstance(value, dict), \
            "value should be either None or a dict"
        if value is None:
            value = {}
        character_pk = Character.objects.first().pk
        abilities = [f"test {ability} recall"
                     for ability in Ability.objects.all()]
        review_types = []
        for index, review_type in enumerate(AVAILABLE_REVIEW_TYPES):
            url = reverse('review_character', args=(character_pk, index))
            type_context = {
                'name': f"{name}_use_{review_type.__name__}",
                'verbose_name': f'<a href="{url}" target="_blank">'
                                f'{review_type.verbose_name}</a>',
                'checked': value.get(
                    f"use_{review_type.__name__}",
                    ReviewManager._meta.get_field(
                        f"use_{review_type.__name__}").get_default()
                )
            }
            has_ability = []
            for ability_code in Ability.ALL_ABILITIES:
                has_ability.append(ability_code in review_type.test_abilities)
            type_context['has_ability'] = has_ability
            review_types.append(type_context)
        return {
            'attrs': attrs,
            'abilities': abilities,
            'review_types': review_types,
        }

    def render(self, name, value, attrs=None, renderer=None):
        return render_to_string(self.template_name,
                                context=self.get_context(name, value, attrs))

    def value_from_datadict(self, data, files, name):
        """
        Returns the kwargs that should be passed into ReviewManger.get
        classmethod
        """
        kwargs = {}
        for review_type in AVAILABLE_REVIEW_TYPES:
            kwargs[f"use_{review_type.__name__}"] =\
                f"{name}_use_{review_type.__name__}" in data
        return kwargs


class ReviewManagerField(forms.Field):
    widget = ReviewManagerWidget

    def prepare_value(self, value):
        if value is None:
            return None
        elif isinstance(value, ReviewManager):
            return value.to_get_kwargs()
        elif isinstance(value, dict):
            return value
        elif isinstance(value, int):
            return ReviewManager.objects.get(pk=value).to_get_kwargs()
        raise TypeError(f'expect None or ReviewManager or dict or, '
                        f'not {type(value)}')


    def to_python(self, value):
        # this is also the validation step
        try:
            return ReviewManager.get(**value)
        except ValidationError as e:
            raise ValidationError(e.messages, code='invalid')
