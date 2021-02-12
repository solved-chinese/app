from django.db import models

from accounts.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='teacher')

    @property
    def display_name(self):
        return self.user.display_name

    def __str__(self):
        return f"Teacher: {self.display_name}"

    def __repr__(self):
        return f"<teacher {self.display_name}>"

    @classmethod
    def of(cls, user):
        """convenient get_or_create"""
        return cls.objects.get_or_create(user=user)[0]
