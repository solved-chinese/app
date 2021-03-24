# Generated by Django 3.1.1 on 2021-03-22 04:57

import re
import logging

from django.db import migrations


def forward(apps, schema_editor):
    MCQuestion = apps.get_model('content', 'MCQuestion')
    for question in MCQuestion.objects.all():
        old_text = question.question
        question.question, cnt_sub= re.subn(r'What does (.*?) mean\?',
                                            r'What does "\1" mean?',
                                            question.question)
        if cnt_sub != 1:
            logging.warning('%r has %d subs: "%s" to "%s"',
                            question, cnt_sub, old_text, question.question)
        else:
            question.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0064_dumbify_memaid_2'),
    ]

    operations = [
        migrations.RunPython(forward, backward, elidable=True)
    ]