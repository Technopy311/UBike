from django.apps import AppConfig
from django.core.signals import request_finished

class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'

    def ready(self):
        # Implicitly connect signals with @receiver decorator C:
        # https://docs.djangoproject.com/en/5.0/topics/signals/#connecting-receiver-functions
        from . import signals