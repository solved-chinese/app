from django.db import models


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
                                   on_delete=models.CASCADE,
                                   null=True)
    question = models.ForeignKey('content.GeneralQuestion',
                                 on_delete=models.SET_NULL,
                                 null=True)
    time = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)
