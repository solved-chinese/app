# Generated by Django 3.1.1 on 2020-11-21 05:22

from django.db import migrations


def update(apps, schema_editor):
    Character = apps.get_model('content', 'Character')
    RadicalInCharacter = apps.get_model('content', 'RadicalInCharacter')
    for c in Character.objects.all():
        for i in range(1, 4):
            radical = getattr(c, f"radical_{i}")
            if radical is None:
                break
            RadicalInCharacter.objects.get_or_create(
                character=c, radical=radical, radical_loc=i)


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20201121_0530'),
    ]

    operations = [
        migrations.RunPython(update)
    ]
