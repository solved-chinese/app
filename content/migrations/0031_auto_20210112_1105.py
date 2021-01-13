# Generated by Django 3.1.1 on 2021-01-12 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0030_auto_20210109_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='dragquestion',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='dragquestion',
            name='question_type',
            field=models.CharField(blank=True, default='custom', max_length=20),
        ),
        migrations.AddField(
            model_name='fitbquestion',
            name='answer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fitbquestion',
            name='extra_information',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fitbquestion',
            name='question_type',
            field=models.CharField(blank=True, default='custom', max_length=20),
        ),
        migrations.AddField(
            model_name='mcquestion',
            name='question_type',
            field=models.CharField(blank=True, default='custom', max_length=20),
        ),
        migrations.AlterField(
            model_name='mcchoice',
            name='linked_value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield'),
        ),
    ]