from django.apps import AppConfig


class EducationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.education'
    
    def ready(self):
        """Importa las señales cuando la aplicación esté lista"""
        import apps.business.education.signals