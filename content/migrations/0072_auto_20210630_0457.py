# Generated by Django 3.1.1 on 2021-06-30 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0071_reversion_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='edit_needed',
            field=models.BooleanField(default=False, help_text='Only admins can edit'),
        ),
        migrations.AddField(
            model_name='radical',
            name='edit_needed',
            field=models.BooleanField(default=False, help_text='Only admins can edit'),
        ),
        migrations.AddField(
            model_name='word',
            name='edit_needed',
            field=models.BooleanField(default=False, help_text='Only admins can edit'),
        ),
        migrations.AddField(
            model_name='wordset',
            name='edit_needed',
            field=models.BooleanField(default=False, help_text='Only admins can edit'),
        ),
    ]