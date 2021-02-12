from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


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
                      " your real name. Leave blank to use your username. "
                      "You may change this later.")
    email = models.EmailField(help_text="Used for resetting your password and "
                                        "receiving notifications.", blank=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} ({self.username})"

    def __repr__(self):
        return f"<user {self.pk}: {self.display_name} ({self.username})>"
