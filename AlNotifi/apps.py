from django.apps import AppConfig


class AlnotifiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AlNotifi'

    def ready(self):
        import AlNotifi.signals
