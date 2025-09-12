from django.urls import path
from apps.business.wildlife.views import ConservationStatusViewSet

# Configuración de rutas para el módulo de Estados de Conservación
# Este módulo maneja toda la lógica relacionada con los estados de conservación de las especies

app_name = 'conservation_status'

urlpatterns = [
    # Listar - Obtiene todos los estados de conservación
    path(
        '',
        ConservationStatusViewSet.as_view({'get': 'list'}),
        name='conservation-status-list'
    ),

    # Crear - Añade un nuevo estado de conservación
    path(
        'create/',
        ConservationStatusViewSet.as_view({'post': 'create'}),
        name='conservation-status-create'
    ),

    # Detalle - Obtiene información detallada de un estado de conservación
    path(
        '<int:pk>/',
        ConservationStatusViewSet.as_view({'get': 'retrieve'}),
        name='conservation-status-detail'
    ),

    # Actualizar - Modifica un estado de conservación existente
    path(
        '<int:pk>/update/',
        ConservationStatusViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='conservation-status-update'
    ),

    # Eliminar - Elimina un estado de conservación
    path(
        '<int:pk>/delete/',
        ConservationStatusViewSet.as_view({'delete': 'destroy'}),
        name='conservation-status-delete'
    ),
]