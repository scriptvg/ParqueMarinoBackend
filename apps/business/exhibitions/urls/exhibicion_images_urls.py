from django.urls import path
from apps.business.exhibitions.views import ExhibicionImageViewSet

# Configuración de rutas para el módulo de Imágenes de Exhibiciones
# Este módulo maneja toda la lógica relacionada con las imágenes de las exhibiciones

app_name = 'exhibicion_images'

urlpatterns = [
    # Listar - Obtiene todas las imágenes de exhibiciones
    path(
        '',
        ExhibicionImageViewSet.as_view({'get': 'list'}),
        name='exhibicion-images-list'
    ),

    # Crear - Añade una nueva imagen de exhibición
    path(
        'create/',
        ExhibicionImageViewSet.as_view({'post': 'create'}),
        name='exhibicion-images-create'
    ),

    # Detalle - Obtiene información detallada de una imagen de exhibición
    path(
        '<int:pk>/',
        ExhibicionImageViewSet.as_view({'get': 'retrieve'}),
        name='exhibicion-images-detail'
    ),

    # Actualizar - Modifica una imagen de exhibición existente
    path(
        '<int:pk>/update/',
        ExhibicionImageViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='exhibicion-images-update'
    ),

    # Eliminar - Elimina una imagen de exhibición
    path(
        '<int:pk>/delete/',
        ExhibicionImageViewSet.as_view({'delete': 'destroy'}),
        name='exhibicion-images-delete'
    ),
]