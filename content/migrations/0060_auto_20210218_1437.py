# Generated by Django 3.1.1 on 2021-02-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0059_auto_20210217_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordset',
            name='jiezi_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='wordset',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]