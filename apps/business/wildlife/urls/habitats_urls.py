from django.urls import path
from apps.business.wildlife.views import HabitatViewSet

# Configuración de rutas para el módulo de Hábitats
# Este módulo maneja toda la lógica relacionada con los hábitats marinos

app_name = 'habitats'

urlpatterns = [
    # Listar - Obtiene todos los hábitats
    path(
        '',
        HabitatViewSet.as_view({'get': 'list'}),
        name='habitat-list'
    ),

    # Crear - Añade un nuevo hábitat
    path(
        'create/',
        HabitatViewSet.as_view({'post': 'create'}),
        name='habitat-create'
    ),

    # Detalle - Obtiene información detallada de un hábitat
    path(
        '<int:pk>/',
        HabitatViewSet.as_view({'get': 'retrieve'}),
        name='habitat-detail'
    ),

    # Actualizar - Modifica un hábitat
    path(
        '<int:pk>/update/',
        HabitatViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='habitat-update'
    ),

    # Eliminar - Elimina un hábitat
    path(
        '<int:pk>/delete/',
        HabitatViewSet.as_view({'delete': 'destroy'}),
        name='habitat-delete'
    ),
]
