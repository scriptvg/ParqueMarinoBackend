from django.contrib import admin
from .models import Documento, HistorialDocumento

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Documentos
    
    Características:
    - Lista personalizada de campos mostrados
    - Filtros por tipo y fecha
    - Búsqueda por título y tags
    - Ordenamiento por fecha de modificación
    - Campos de solo lectura para fechas
    """
    
    list_display = ['titulo', 'tipo', 'version', 'creado_por', 'fecha_modificacion']
    list_filter = ['tipo', 'fecha_creacion', 'fecha_modificacion']
    search_fields = ['titulo', 'descripcion', 'tags']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['-fecha_modificacion']
    
    fieldsets = [
        ('Información Principal', {
            'fields': ['titulo', 'tipo', 'descripcion']
        }),
        ('Archivo', {
            'fields': ['archivo']
        }),
        ('Metadatos', {
            'fields': ['version', 'tags', 'creado_por']
        }),
        ('Fechas', {
            'fields': ['fecha_creacion', 'fecha_modificacion'],
            'classes': ['collapse']
        })
    ]

@admin.register(HistorialDocumento)
class HistorialDocumentoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Historial de Documentos
    
    Características:
    - Vista detallada del historial de cambios
    - Filtros por tipo de cambio y fecha
    - Búsqueda por descripción
    - Campos de solo lectura para preservar la integridad del historial
    """
    
    list_display = ['documento', 'tipo_cambio', 'usuario', 'fecha']
    list_filter = ['tipo_cambio', 'fecha', 'usuario']
    search_fields = ['documento__titulo', 'descripcion']
    readonly_fields = ['documento', 'usuario', 'fecha', 'tipo_cambio', 'descripcion', 'version_anterior']
    ordering = ['-fecha']
    
    def has_add_permission(self, request):
        """Deshabilita la creación manual de registros de historial"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Deshabilita la edición de registros de historial"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Deshabilita la eliminación de registros de historial"""
        return False
