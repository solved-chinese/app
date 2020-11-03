from django.db import models

from jiezi.utils.mixins import StrDefaultReprMixin


class Report(models.Model, StrDefaultReprMixin):
    user = models.ForeignKey('accounts.User', null=True,
                             on_delete=models.SET_NULL)
    origin = models.CharField(max_length=100)
    description_1 = models.CharField(max_length=100)
    description_2 = models.TextField()

    def __repr__(self):
        return f'<Report on {self.origin}: {self.description_1}>'

    class Meta:
        ordering = ['origin']