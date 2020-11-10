from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .managers import JieziUserManager, factory_message_manager_of_user, \
    MessageManager


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
    is_guest = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    # testers will be filtered and will not count into stats
    is_tester = models.BooleanField(default=False)

    objects = JieziUserManager()

    def save(self, *args, **kwargs):
        if self.is_guest:
            self.display_name = 'Guest'
        elif not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def notify(self, subject, content=""):
        msg = Message(receiver=self, subject=subject, content=content)
        msg.save()
        return msg

    @property
    def unread_message_count(self):
        return Message.of(self).count_unread()

    REMOVE_TESTER_FILTER_KWARGS = {'is_tester': False, 'is_guest': False}
    REMOVE_TESTER_EXCLUDE_KWARGS = {'username__startswith': 'test_'}
    @staticmethod
    def remove_testers(queryset):
        return queryset.filter(**User.REMOVE_TESTER_FILTER_KWARGS)\
            .exclude(**User.REMOVE_TESTER_EXCLUDE_KWARGS)

    def __str__(self):
        return f"{self.display_name} ({self.username})"

    def __repr__(self):
        return f"<user {self.pk}: {self.display_name} ({self.username})>"


class Message(models.Model):
    _sender = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=True, default=None, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='+')
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    subject = models.TextField(blank=False)
    content = models.TextField(blank=True)

    objects = MessageManager()
    of = factory_message_manager_of_user

    class Meta:
        ordering = ['-time']

    def read(self):
        self.is_read = True
        self.save()

    @property
    def sender(self):
        return self._sender.display_name if self._sender else \
            'the solved team'
