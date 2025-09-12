from django.urls import path
from apps.business.wildlife.views import AnimalViewSet

# Configuración de rutas para el módulo de Animales
# Este módulo maneja toda la lógica relacionada con los animales marinos

app_name = 'animals'

urlpatterns = [
    # Listar - Obtiene todos los animales
    path(
        '',
        AnimalViewSet.as_view({'get': 'list'}),
        name='animal-list'
    ),

    # Crear - Añade un nuevo animal
    path(
        'create/',
        AnimalViewSet.as_view({'post': 'create'}),
        name='animal-create'
    ),

    # Detalle - Obtiene información detallada de un animal
    path(
        '<int:pk>/',
        AnimalViewSet.as_view({'get': 'retrieve'}),
        name='animal-detail'
    ),

    # Actualizar - Modifica un animal
    path(
        '<int:pk>/update/',
        AnimalViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='animal-update'
    ),

    # Eliminar - Elimina un animal
    path(
        '<int:pk>/delete/',
        AnimalViewSet.as_view({'delete': 'destroy'}),
        name='animal-delete'
    ),
]
