from django.db import models


class RadicalInCharacter(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    radical = models.ForeignKey('Radical', on_delete=models.CASCADE)
    radical_loc = models.IntegerField()

    class Meta:
        ordering = ['radical_loc']
        unique_together = ['character', 'radical']
