# Generated by Django 3.1.1 on 2021-01-05 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_auto_20210103_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='radical',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='wordset',
            options={'ordering': ['id']},
        ),
    ]