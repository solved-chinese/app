from django.core.exceptions import ValidationError
from django.db import models


__all__ = ['ReviewableMixin', 'ReviewableObject']


class ReviewableMixin:
    def get_reviewable_object(self):
        d = {self.__class__.__name__.lower(): self}
        return ReviewableObject.objects.get_or_create(**d)[0]


class ReviewableObject(models.Model):
    radical = models.OneToOneField('Radical', blank=True, null=True,
                                   related_name='reviewable',
                                   on_delete=models.CASCADE)
    character = models.OneToOneField('Character', blank=True, null=True,
                                     related_name='reviewable',
                                     on_delete=models.CASCADE)
    word = models.OneToOneField('Word', blank=True, null=True,
                                related_name='reviewable',
                                on_delete=models.CASCADE)

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
