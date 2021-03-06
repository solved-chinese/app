# Generated by Django 3.1.1 on 2020-11-01 10:12

import accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20201017_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, help_text='This is the name displayed to others. We recommend using your real name. Leave blank to use your username. You may change this later.', max_length=30, validators=[django.core.validators.MinLengthValidator(4), accounts.models.DisplayNameValidator]),
        ),
    ]
