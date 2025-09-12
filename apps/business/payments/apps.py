from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    """Configuración de la aplicación de pagos
    
    Esta clase define la configuración básica de la aplicación de pagos,
    incluyendo el nombre predeterminado y la etiqueta para el panel de
    administración.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.payments'
    verbose_name = 'Gestión de Pagos'
    
    def ready(self):
        """Importa las señales cuando la aplicación esté lista"""
        import apps.business.payments.signals