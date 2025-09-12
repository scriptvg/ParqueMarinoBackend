from django.urls import path
from apps.business.exhibitions.views import ExhibicionFactsViewSet

# Configuración de rutas para el módulo de Datos de Exhibiciones
# Este módulo maneja toda la lógica relacionada con los datos interesantes de las exhibiciones

app_name = 'exhibicion_facts'

urlpatterns = [
    # Listar - Obtiene todos los datos de exhibiciones
    path(
        '',
        ExhibicionFactsViewSet.as_view({'get': 'list'}),
        name='exhibicion-facts-list'
    ),

    # Crear - Añade un nuevo dato de exhibición
    path(
        'create/',
        ExhibicionFactsViewSet.as_view({'post': 'create'}),
        name='exhibicion-facts-create'
    ),

    # Detalle - Obtiene información detallada de un dato de exhibición
    path(
        '<int:pk>/',
        ExhibicionFactsViewSet.as_view({'get': 'retrieve'}),
        name='exhibicion-facts-detail'
    ),

    # Actualizar - Modifica un dato de exhibición existente
    path(
        '<int:pk>/update/',
        ExhibicionFactsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='exhibicion-facts-update'
    ),

    # Eliminar - Elimina un dato de exhibición
    path(
        '<int:pk>/delete/',
        ExhibicionFactsViewSet.as_view({'delete': 'destroy'}),
        name='exhibicion-facts-delete'
    ),
]