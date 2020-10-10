class CleanBeforeSaveMixin:
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StrDefaultReprMixin:
    def __str__(self):
        return repr(self)
