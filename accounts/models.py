from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .managers import JieziUserManager


@deconstructible
class DisplayNameValidator(validators.RegexValidator):
    regex = r'^[\w]+[ \w.-]+[\w]+\Z'
    message = _(
        'Enter a valid display name. This value may contain only letters, '
        'numbers, and /./- characters. Space may appear only in the middle'
    )
    flags = 0


class User(AbstractUser):
    display_name = models.CharField(max_length=30, blank=True,
            validators=[MinLengthValidator(4), DisplayNameValidator],
            help_text="This is the name displayed to others. We recommend using"
                      " your real name. You may change this later.")
    email = models.EmailField(help_text="Used for resetting your password and "
                                        "receiving notifications.", blank=True)
    is_guest = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = JieziUserManager()

    def get_display_name(self):
        if self.is_guest:
            return 'Guest'
        elif self.display_name:
            return self.display_name
        else:
            return self.username
