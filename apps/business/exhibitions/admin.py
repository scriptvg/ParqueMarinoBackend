from django.contrib import admin
from .models import (
    Exhibicion,
    ExhibicionImage,
    ExhibicionFacts,
    ExhibicionDescription,
    ExhibicionButtons
)

@admin.register(Exhibicion)
class ExhibicionAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Exhibiciones.
    
    Define cómo se mostrarán y gestionarán las exhibiciones en el
    panel de administración de Django.
    """
    
    list_display = ('value', 'label', 'title')
    search_fields = ('value', 'label', 'title')
    ordering = ('value',)

@admin.register(ExhibicionImage)
class ExhibicionImageAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Imágenes de Exhibiciones."""
    
    list_display = ('exhibicion', 'image', 'created_at', 'updated_at')
    list_filter = ('exhibicion', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ExhibicionFacts)
class ExhibicionFactsAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Datos de Exhibiciones."""
    
    list_display = ('exhibicion', 'fact')
    list_filter = ('exhibicion',)
    search_fields = ('fact',)

@admin.register(ExhibicionDescription)
class ExhibicionDescriptionAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Descripciones de Exhibiciones."""
    
    list_display = ('exhibicion', 'description')
    list_filter = ('exhibicion',)
    search_fields = ('description',)

@admin.register(ExhibicionButtons)
class ExhibicionButtonsAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para Botones de Exhibiciones."""
    
    list_display = ('exhibicion', 'label', 'link')
    list_filter = ('exhibicion',)
    search_fields = ('label', 'link')
