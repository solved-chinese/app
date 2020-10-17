# Generated by Django 3.1.1 on 2020-10-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_auto_20201013_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.CharField(blank=True, help_text=' Please enter your school name, region, and country. E.g.\n        "St. Mark\'s School, Massachusetts, United States." ', max_length=200),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school_description',
            field=models.TextField(blank=True, help_text='Please describe the textbook / curriculum you use. E.g. \n        “Integrated Chinese,” “HSK Standard Course,” or “a self-written IB \n        curriculum.” You may also add any other relevant information.', max_length=2000, verbose_name='Your curriculum'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='wechat_id',
            field=models.CharField(blank=True, help_text='Optional. Used for us to contact you, if you’d like.', max_length=40, verbose_name='Wechat account id'),
        ),
    ]