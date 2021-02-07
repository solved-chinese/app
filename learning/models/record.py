from django.db import models
from django.core.exceptions import ValidationError


class Record(models.Model):
    class Action(models.IntegerChoices):
        WRONG_ANSWER = 1
        CORRECT_ANSWER = 2
        LEARN = 3
        RELEARN = 4
    action = models.SmallIntegerField(choices=Action.choices,
                                      default=0)
    user = models.ForeignKey('accounts.User',
                             on_delete=models.SET_NULL,
                             null=True,
                             help_text="None means AnonymousUsers")
    learning_process = models.ForeignKey('LearningProcess',
                                         on_delete=models.SET_NULL,
                                         null=True)
    reviewable = models.ForeignKey('content.ReviewableObject',
                                   on_delete=models.SET_NULL,
                                   null=True)
    question = models.ForeignKey('content.GeneralQuestion',
                                 on_delete=models.SET_NULL,
                                 null=True)
    time = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ('-time',)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.data.update({
                'initial_data': dict(
                    user=repr(self.user),
                    learning_process=repr(self.learning_process),
                    reviewable=repr(self.reviewable),
                    question=repr(self.question),
                    action=self.get_action_display(),
                )
            })
        else:
            raise ValidationError("Record not editable")
        super().save(*args, **kwargs)

