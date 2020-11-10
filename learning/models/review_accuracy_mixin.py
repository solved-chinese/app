from decimal import Decimal

from django.db import models


class ReviewAccuracyAbstractModel(models.Model):
    accuracy = models.FloatField(null=True)
    total_attempts = models.PositiveSmallIntegerField(default=0)
    correct_attempts = models.PositiveSmallIntegerField(default=0)

    def test_review_update(self, is_correct, save=True):
        self.total_attempts += 1
        if is_correct:
            self.correct_attempts += 1
        self.accuracy = self.correct_attempts / self.total_attempts
        if save:
            self.save()

    class Meta:
        abstract = True
