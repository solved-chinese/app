from django.db import models
from collections import namedtuple

from jiezi.utils.mixins import CleanBeforeSaveMixin

RawAbility = namedtuple('RawAbility',
                        'name default_in_a_row_required max_in_a_row_required')
RAW_ABILITIES = [
    RawAbility('definition', 2, 2),
    RawAbility('form', 1, 1),
    RawAbility('pronunciation', 2, 2),
]


class Ability(CleanBeforeSaveMixin, models.Model):
    DEFINITION = 0
    FORM = 1
    PRONUNCIATION = 2

    ALL_ABILITIES = [DEFINITION, FORM, PRONUNCIATION]
    CHOICES = [
        (DEFINITION, 'definition'),
        (FORM, 'form'),
        (PRONUNCIATION, 'pronunciation'),
    ]
    code = models.PositiveSmallIntegerField(choices=CHOICES, unique=True)

    def __str__(self):
        return RAW_ABILITIES[self.code].name

    def __repr__(self):
        return f"<Ability {self.pk} code={self.code} name={str(self)}>"

    @property
    def max_in_a_row_requied(self):
        return RAW_ABILITIES[self.code].max_in_a_row_required

    @property
    def default_in_a_row_required(self):
        return RAW_ABILITIES[self.code].default_in_a_row_required

    @classmethod
    def of(cls, value):
        return cls.objects.get_or_create(code=value)[0]


def init_abilities(sender, **kwargs):
    """
    This is executed after each migration to guarantee that there are
    the correct abilities in database
    """
    good_pks = []
    for ability in Ability.ALL_ABILITIES:
        good_pks.append(Ability.of(ability).pk)
    Ability.objects.exclude(pk__in=good_pks).delete()
