from django.urls import path
from apps.business.documents.views import HistorialDocumentoViewSet

# Configuración de rutas para el módulo de Historial de Documentos
# Este módulo maneja toda la lógica relacionada con el historial de documentos

app_name = 'historial_documentos'

urlpatterns = [
    # Listar - Obtiene todo el historial de documentos
    path(
        '',
        HistorialDocumentoViewSet.as_view({'get': 'list'}),
        name='historial-documentos-list'
    ),

    # Detalle - Obtiene información detallada de un registro de historial
    path(
        '<int:pk>/',
        HistorialDocumentoViewSet.as_view({'get': 'retrieve'}),
        name='historial-documentos-detail'
    ),
]