from django.apps import AppConfig


class WildlifeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.wildlife'
    
    def ready(self):
        """Importa las señales cuando la aplicación esté lista"""
        import apps.business.wildlife.signals