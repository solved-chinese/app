# Generated by Django 3.1.1 on 2020-10-29 07:54

from django.db import migrations, models
import django.db.models.deletion
import learning.models.review_manager


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0019_auto_20201029_0652'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_DefinitionMCAnswerField', models.BooleanField(default=True)),
                ('use_DefinitionMCAnswerCharacter', models.BooleanField(default=True)),
                ('use_PinyinMC', models.BooleanField(default=True)),
                ('use_DefinitionTOF', models.BooleanField(default=True)),
                ('use_PinyinTOF', models.BooleanField(default=True)),
                ('use_DefinitionFITB', models.BooleanField(default=True)),
                ('use_PinyinFITB', models.BooleanField(default=True)),
                ('monitored_abilities', models.ManyToManyField(related_name='_reviewmanager_monitored_abilities_+', to='learning.Ability')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='learningprocess',
            name='review_manager',
            field=models.ForeignKey(default=learning.models.review_manager.ReviewManager.get_default_pk, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='learning.reviewmanager'),
        ),
    ]
