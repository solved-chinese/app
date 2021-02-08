from django.db import models


class UserReviewableManager(models.Manager):
    def get_or_create(self, defaults=None, **kwargs):
        obj, created = super().get_or_create(defaults=defaults, **kwargs)
        if created:
            obj.data = {
                'learning_process': []
            }
            obj.save()
        return obj, created


class UserReviewable(models.Model):
    BONUS_THRESHOLD = 3

    user = models.ForeignKey('accounts.User',
                             on_delete=models.CASCADE)
    reviewable = models.ForeignKey('content.ReviewableObject',
                                   on_delete=models.CASCADE)
    learned_related_reviewables = models.ManyToManyField(
        'content.ReviewableObject',
        related_name='+',
    )
    data = models.JSONField(default=dict)

    objects = UserReviewableManager()

    def learn_related(self, reviewable):
        """ returns: whether this reviewable could be add as bonus """
        self.learned_related_reviewables.add(reviewable)
        if self.learned_related_reviewables.count() >= self.BONUS_THRESHOLD \
                and not self.data['learning_process']:
            return True
        return False

    def bind_to_process(self, process):
        if self.reviewable.word or not self.data['learning_process']:
            self.data['learning_process'].append(process.pk)
            self.save()
        return False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<UR {self.pk}: {repr(self.user)}'s {repr(self.reviewable)}>"
