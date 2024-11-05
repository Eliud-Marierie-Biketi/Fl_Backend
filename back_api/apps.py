from django.apps import AppConfig


class BackApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'back_api'

    def ready(self):
        # Import signals to ensure they are registered
        import back_api.signals
