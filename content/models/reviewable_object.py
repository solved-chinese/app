from django.core.exceptions import ValidationError
from django.db import models


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




"""
MC single choice for now
is_correct: True / False
link: <C0001你#>'s pinyin field (ni)
overwrite: ni
weighting: 1 (regular wrong answer), 5 (somewhat misleading answer), 
    100 (very misleading) 

10 incorrect answers, 1 correct answer
randomly draw 3 incorrect + 1 correct
ABCD
ABEF
"""