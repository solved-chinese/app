from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse

from .general_content_model import AdminUrlMixin


__all__ = ['ReviewableMixin', 'ReviewableObject']


class ReviewableMixin:
    def render(self):
        return {
            'action': 'display',
            'content': {'type': self.__class__.__name__.lower(),
                        'qid': self.pk}
        }

    def get_absolute_url(self):
        return reverse(f'{self.__class__.__name__.lower()}_display',
                       args=(self.pk,))

    def get_reviewable_object(self):
        d = {self.__class__.__name__.lower(): self}
        return ReviewableObject.objects.get_or_create(**d)[0]


class ReviewableObject(AdminUrlMixin, models.Model):
    radical = models.OneToOneField('Radical', blank=True, null=True,
                                   related_name='reviewable',
                                   on_delete=models.CASCADE)
    character = models.OneToOneField('Character', blank=True, null=True,
                                     related_name='reviewable',
                                     on_delete=models.CASCADE)
    word = models.OneToOneField('Word', blank=True, null=True,
                                related_name='reviewable',
                                on_delete=models.CASCADE)

    def get_bonuses(self):
        # for now allowing only 1 bonus per word, none otherwise
        from .radical import Radical
        if self.word:
            bonuses = [
                *self.word.characters.distinct(),
                *Radical.objects.filter(is_learnable=True,
                                        character__word=self.word).distinct(),
            ]
            bonuses = bonuses[:1]
            return [bonus.get_reviewable_object() for bonus in bonuses]
        elif self.character:
            return []
            # return [radical.get_reviewable_object()
            #         for radical in self.character.radicals.distinct()]
        else:
            return []

    def clean(self):
        i = iter([self.radical, self.character, self.word])
        if not any(i) or any(i):
            raise ValidationError(
                f"radical {self.radical} character "
                f"{self.character} word {self.word} not only one exists")

    def save(self, *args, **kwargs):
        """ makes sure only and only one real object """
        if self._state.adding:
            self.clean()
        else:
            raise Exception("reviewable object is not mutable")
        super().save(*args, **kwargs)

    @property
    def concrete_object(self):
        return self.word or self.character or self.radical

    def __repr__(self):
        return f"<RO of {repr(self.concrete_object)}>"

    def __str__(self):
        return repr(self)

    @property
    def definition(self):
        if self.radical:
            return self.radical.definition
        return self.concrete_object.full_definition

    def __getattr__(self, item):
        if item in ('render',):
            return getattr(self.concrete_object, item)
        return super().__getattribute__(item)
