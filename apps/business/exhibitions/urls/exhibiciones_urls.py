from django.urls import path
from apps.business.exhibitions.views import ExhibicionViewSet

# Configuración de rutas para el módulo de Exhibiciones
# Este módulo maneja toda la lógica relacionada con las exhibiciones del parque

app_name = 'exhibiciones'

urlpatterns = [
    # Listar - Obtiene todas las exhibiciones
    path(
        '',
        ExhibicionViewSet.as_view({'get': 'list'}),
        name='exhibiciones-list'
    ),

    # Crear - Añade una nueva exhibición
    path(
        'create/',
        ExhibicionViewSet.as_view({'post': 'create'}),
        name='exhibiciones-create'
    ),

    # Detalle - Obtiene información detallada de una exhibición
    path(
        '<int:pk>/',
        ExhibicionViewSet.as_view({'get': 'retrieve'}),
        name='exhibiciones-detail'
    ),

    # Detalles completos - Obtiene todos los detalles de una exhibición
    path(
        '<int:pk>/full_details/',
        ExhibicionViewSet.as_view({'get': 'full_details'}),
        name='exhibiciones-full-details'
    ),

    # Actualizar - Modifica una exhibición existente
    path(
        '<int:pk>/update/',
        ExhibicionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='exhibiciones-update'
    ),

    # Eliminar - Elimina una exhibición
    path(
        '<int:pk>/delete/',
        ExhibicionViewSet.as_view({'delete': 'destroy'}),
        name='exhibiciones-delete'
    ),
]