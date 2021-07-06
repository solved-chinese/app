from django.db import models

from accounts.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='student')
    klass = models.ForeignKey('classroom.Class', on_delete=models.SET_NULL,
                              related_name='students',
                              related_query_name='student',
                              null=True, blank=True)

    def join_class(self, class_object):
        assert self.klass is None, \
            f"You can't join a class while already in a class ({self.klass})"
        self.klass = class_object
        self.save()

    def quit_class(self):
        self.klass = None
        self.save()

    @property
    def display_name(self) -> str:
        return self.user.display_name

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<student of {self.user}>"

    @classmethod
    def of(cls, user):
        """convenient get_or_create"""
        return cls.objects.get_or_create(user=user)[0]
