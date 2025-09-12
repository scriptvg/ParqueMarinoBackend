from django.contrib import admin
from .models import Ticket, Visit

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Tickets.
    
    Personaliza la visualización y gestión de tickets en el panel de administración.
    """
    list_display = [
        'name',
        'price',
        'currency',
        'total_slots',
        'occupied_slots'
    ]
    list_filter = ['currency']
    search_fields = ['name', 'description']
    readonly_fields = ['occupied_slots']
    ordering = ['name']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Visitas.
    
    Personaliza la visualización y gestión de visitas en el panel de administración.
    """
    list_display = [
        'day',
        'total_slots',
        'occupied_slots'
    ]
    list_filter = ['day']
    readonly_fields = ['occupied_slots']
    ordering = ['-day']

    def get_readonly_fields(self, request, obj=None):
        """Define campos de solo lectura según si es creación o edición.
        
        Args:
            request: Solicitud HTTP
            obj: Instancia del modelo o None si es creación
            
        Returns:
            list: Lista de campos de solo lectura
        """
        if obj:  # Si es edición
            return ['day', 'occupied_slots']
        return ['occupied_slots']  # Si es creación
