from django.urls import path
from apps.business.documents.views import DocumentoViewSet

# Configuración de rutas para el módulo de Documentos
# Este módulo maneja toda la lógica relacionada con los documentos del sistema

app_name = 'documentos'

urlpatterns = [
    # Listar - Obtiene todos los documentos
    path(
        '',
        DocumentoViewSet.as_view({'get': 'list'}),
        name='documentos-list'
    ),

    # Crear - Añade un nuevo documento
    path(
        'create/',
        DocumentoViewSet.as_view({'post': 'create'}),
        name='documentos-create'
    ),

    # Detalle - Obtiene información detallada de un documento
    path(
        '<int:pk>/',
        DocumentoViewSet.as_view({'get': 'retrieve'}),
        name='documentos-detail'
    ),

    # Actualizar - Modifica un documento existente
    path(
        '<int:pk>/update/',
        DocumentoViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='documentos-update'
    ),

    # Eliminar - Elimina un documento
    path(
        '<int:pk>/delete/',
        DocumentoViewSet.as_view({'delete': 'destroy'}),
        name='documentos-delete'
    ),
]