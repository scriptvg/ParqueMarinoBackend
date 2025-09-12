from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para registros de auditoría.
    
    Esta clase personaliza cómo se muestran y gestionan los registros de
    auditoría en el panel de administración de Django.
    
    Attributes:
        list_display: Campos a mostrar en la lista de registros.
        list_filter: Campos por los que se puede filtrar.
        search_fields: Campos en los que se puede buscar.
        readonly_fields: Campos que no se pueden modificar.
        ordering: Orden por defecto de los registros.
    """
    
    list_display = [
        'timestamp',
        'user',
        'action',
        'model',
        'record_id',
    ]
    
    list_filter = [
        'timestamp',
        'user',
        'action',
        'model',
    ]
    
    search_fields = [
        'user__username',
        'action',
        'model',
        'details',
    ]
    
    readonly_fields = [
        'timestamp',
        'user',
        'action',
        'model',
        'record_id',
        'details',
    ]
    
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Deshabilita la creación manual de registros."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Deshabilita la modificación de registros."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Deshabilita la eliminación de registros."""
        return False
