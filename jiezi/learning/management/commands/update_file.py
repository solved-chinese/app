from django.core.management.base import BaseCommand
from learning.models import Radical, Character
import jiezi.settings as settings
import os
import PIL.Image

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for radical in Radical.objects.all():
            radical.mnemonic_image.open()
            radical.save()
            # radical.mnemonic_image.save()
        # for character in Character.objects.all():
        #     character.small_color_coded.open()
        #     character.stroke_order_image.open()
        print('done')