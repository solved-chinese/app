# Generated by Django 3.1.1 on 2021-04-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0005_auto_20210326_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='school',
            field=models.CharField(default='__empty__', max_length=100),
            preserve_default=False,
        ),
    ]