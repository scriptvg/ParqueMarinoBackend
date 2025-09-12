from django.urls import path
from apps.business.infrastructure.views import SectionsViewSet

# Configuración de rutas para el módulo de Secciones
# Este módulo maneja toda la lógica relacionada con las secciones del parque marino

app_name = 'sections'

urlpatterns = [
    # Listar - Obtiene todas las secciones
    path(
        '',
        SectionsViewSet.as_view({'get': 'list'}),
        name='sections-list'
    ),

    # Crear - Añade una nueva sección
    path(
        'create/',
        SectionsViewSet.as_view({'post': 'create'}),
        name='sections-create'
    ),

    # Detalle - Obtiene información detallada de una sección
    path(
        '<int:pk>/',
        SectionsViewSet.as_view({'get': 'retrieve'}),
        name='sections-detail'
    ),

    # Actualizar - Modifica una sección existente
    path(
        '<int:pk>/update/',
        SectionsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='sections-update'
    ),

    # Eliminar - Elimina una sección
    path(
        '<int:pk>/delete/',
        SectionsViewSet.as_view({'delete': 'destroy'}),
        name='sections-delete'
    ),
]