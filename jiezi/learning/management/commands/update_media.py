from django.core.management.base import BaseCommand
from learning.models import Radical, Character
import jiezi.settings as settings
import os

class Command(BaseCommand):
    help = 'update media'

    def handle(self, *args, **kwargs):
        for radical in Radical.objects.all():
            name = 'radical_mnemonic/R%04d.png'%radical.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path) :
                radical.mnemonic_image=name
                radical.save()
            else:
                print(f'not found {radical}s radical_mnemonic png')
        for character in Character.objects.all():
            name = 'animated_stroke_order/C%04d.gif' % character.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path):
                character.stroke_order_image = name
                character.save()
            else:
                print(f'not found {character}‘s animated_stroke_order gif')
        for character in Character.objects.all():
            name = 'color_coded_characters/C%04d.png' % character.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path):
                character.color_coded_image = name
                character.save()
            else:
                print(f'not found {character}‘s color_coded_characters png')