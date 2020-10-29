from django.db import models

from jiezi.utils.mixins import CleanBeforeSaveMixin


class Ability(CleanBeforeSaveMixin, models.Model):
    DEFINITION = 0
    FORM = 1
    PRONUNCIATION = 2

    ALL_ABILITIES = [DEFINITION, FORM, PRONUNCIATION]
    ABILITY2MAX_IN_A_ROW_REQUIRED = {
        DEFINITION: 2,
        FORM: 1,
        PRONUNCIATION: 2,
    }
    ABILITY2DEFAULT_IN_A_ROW_REQUIRED = {
        DEFINITION: 2,
        FORM: 1,
        PRONUNCIATION: 2,
    }
    CHOICES = [
        (DEFINITION, 'definition'),
        (FORM, 'form'),
        (PRONUNCIATION, 'pronunciation'),
    ]
    code = models.PositiveSmallIntegerField(choices=CHOICES, unique=True)

    @property
    def max_in_a_row_requied(self):
        return self.ABILITY2MAX_IN_A_ROW_REQUIRED[self.code]

    @property
    def default_in_a_row_required(self):
        return self.ABILITY2DEFAULT_IN_A_ROW_REQUIRED[self.code]

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
