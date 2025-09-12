from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.documents'
    
    def ready(self):
        """Importa las señales cuando la aplicación esté lista"""
        import apps.business.documents.signals