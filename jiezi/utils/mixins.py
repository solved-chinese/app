from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render


class IsTeacherMixin(UserPassesTestMixin):
    permission_denied_message = "Only teachers can access this page"
    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_teacher


class IsStudentMixin(UserPassesTestMixin):
    permission_denied_message = "Only students can access this page"

    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_student


class CleanBeforeSaveMixin:
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StrDefaultReprMixin:
    def __str__(self):
        return repr(self)
