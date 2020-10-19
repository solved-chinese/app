from uuid import uuid4

from django.contrib.auth.models import UserManager
from django.db import models

import accounts.models


class JieziUserManager(UserManager):
    def create_guest_student(self):
        """This doesn't create Student object tho"""
        user = self.create_user(f"test_user_{uuid4().hex}",
                                is_guest=True, is_student=True)
        return user


class MessageManager(models.Manager):
    def __init__(self, receiver=None, *args, **kwargs):
        self._receiver = receiver
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self._receiver is not None:
            queryset = queryset.filter(receiver=self._receiver)
        return queryset

    def count_unread(self):
        return self.get_queryset().filter(is_read=False).count()

    @classmethod
    def of(cls, model, receiver=None):
        manager = cls(receiver=receiver)
        manager.model = model
        return manager


def factory_message_manager_of_user(receiver):
    return MessageManager.of(accounts.models.Message, receiver)
