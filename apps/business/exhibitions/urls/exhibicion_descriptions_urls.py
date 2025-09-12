from django.urls import path
from apps.business.exhibitions.views import ExhibicionDescriptionViewSet

# Configuración de rutas para el módulo de Descripciones de Exhibiciones
# Este módulo maneja toda la lógica relacionada con las descripciones de las exhibiciones

app_name = 'exhibicion_descriptions'

urlpatterns = [
    # Listar - Obtiene todas las descripciones de exhibiciones
    path(
        '',
        ExhibicionDescriptionViewSet.as_view({'get': 'list'}),
        name='exhibicion-descriptions-list'
    ),

    # Crear - Añade una nueva descripción de exhibición
    path(
        'create/',
        ExhibicionDescriptionViewSet.as_view({'post': 'create'}),
        name='exhibicion-descriptions-create'
    ),

    # Detalle - Obtiene información detallada de una descripción de exhibición
    path(
        '<int:pk>/',
        ExhibicionDescriptionViewSet.as_view({'get': 'retrieve'}),
        name='exhibicion-descriptions-detail'
    ),

    # Actualizar - Modifica una descripción de exhibición existente
    path(
        '<int:pk>/update/',
        ExhibicionDescriptionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='exhibicion-descriptions-update'
    ),

    # Eliminar - Elimina una descripción de exhibición
    path(
        '<int:pk>/delete/',
        ExhibicionDescriptionViewSet.as_view({'delete': 'destroy'}),
        name='exhibicion-descriptions-delete'
    ),
]