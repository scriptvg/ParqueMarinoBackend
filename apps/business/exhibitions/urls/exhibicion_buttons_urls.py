from django.urls import path
from apps.business.exhibitions.views import ExhibicionButtonsViewSet

# Configuración de rutas para el módulo de Botones de Exhibiciones
# Este módulo maneja toda la lógica relacionada con los botones de las exhibiciones

app_name = 'exhibicion_buttons'

urlpatterns = [
    # Listar - Obtiene todos los botones de exhibiciones
    path(
        '',
        ExhibicionButtonsViewSet.as_view({'get': 'list'}),
        name='exhibicion-buttons-list'
    ),

    # Crear - Añade un nuevo botón de exhibición
    path(
        'create/',
        ExhibicionButtonsViewSet.as_view({'post': 'create'}),
        name='exhibicion-buttons-create'
    ),

    # Detalle - Obtiene información detallada de un botón de exhibición
    path(
        '<int:pk>/',
        ExhibicionButtonsViewSet.as_view({'get': 'retrieve'}),
        name='exhibicion-buttons-detail'
    ),

    # Actualizar - Modifica un botón de exhibición existente
    path(
        '<int:pk>/update/',
        ExhibicionButtonsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='exhibicion-buttons-update'
    ),

    # Eliminar - Elimina un botón de exhibición
    path(
        '<int:pk>/delete/',
        ExhibicionButtonsViewSet.as_view({'delete': 'destroy'}),
        name='exhibicion-buttons-delete'
    ),
]