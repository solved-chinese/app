import django.contrib.auth.mixins


class TeacherOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only teachers can access this page"
    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_teacher


class StudentOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only students can access this page"

    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_student


class RegisteredStudentOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only registered students can access this page"

    def test_func(self):
        return self.request.user.is_authenticated \
               and not self.request.user.is_guest \
               and self.request.user.is_student


class RegisteredOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only registered users can access this page."

    def test_func(self):
        return self.request.user.is_authenticated \
               and not self.request.user.is_guest


class CleanBeforeSaveMixin:
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StrDefaultReprMixin:
    def __str__(self):
        return repr(self)

    def __repr__(self):
        raise NotImplementedError("__repr__ should be overriden to prevent"
                                  "RecurssionError")
