# Generated by Django 3.1.1 on 2021-03-17 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]