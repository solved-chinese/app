# Generated by Django 3.1.1 on 2021-02-17 08:03

from django.db import migrations, models

def forward(apps, schema_editor):
    WordSet = apps.get_model('content', 'WordSet')
    for wordset in WordSet.objects.all():
        wordset.jiezi_id = f"j{wordset.id}"
        wordset.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0058_wordset_jiezi_id'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
        migrations.AlterField(
            model_name='wordset',
            name='jiezi_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
