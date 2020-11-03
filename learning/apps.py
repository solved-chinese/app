from django.apps import AppConfig
from django.db.models.signals import post_migrate


class LearningConfig(AppConfig):
    name = 'learning'

    def ready(self):
        from learning.models.ability import init_abilities
        post_migrate.connect(init_abilities, sender=self)
