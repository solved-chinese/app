from django.db import models


class Record(models.Model):
    user = models.ForeignKey('accounts.User',
                             on_delete=models.SET_NULL,
                             null=True,
                             help_text="None means AnonymousUsers")
    question = models.ForeignKey('content.GeneralQuestion',
                                 on_delete=models.CASCADE)
    question_is_correct = models.BooleanField()
    question_data = models.TextField(blank=True)
