# Generated by Django 3.1.1 on 2020-10-11 06:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0011_auto_20201011_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningprocess',
            name='review_field_index',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(1)]),
        ),
    ]
