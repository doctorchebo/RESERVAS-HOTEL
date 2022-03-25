from django.apps import AppConfig


class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RESERVAS'

    def ready(self) -> None:    
        import RESERVAS.signals.handlers
