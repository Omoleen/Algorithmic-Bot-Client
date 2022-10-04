from django.apps import AppConfig


class WiseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wiseapp'

    def ready(self):
        import wiseapp.signals
