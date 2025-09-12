from django.urls import path
from apps.business.infrastructure.views import Habitats_ViewSet

# Configuración de rutas para el módulo de Hábitats de Infraestructura
# Este módulo maneja toda la lógica relacionada con los hábitats de infraestructura del parque

app_name = 'infrastructure_habitats'

urlpatterns = [
    # Listar - Obtiene todos los hábitats de infraestructura
    path(
        '',
        Habitats_ViewSet.as_view({'get': 'list'}),
        name='infrastructure-habitats-list'
    ),

    # Crear - Añade un nuevo hábitat de infraestructura
    path(
        'create/',
        Habitats_ViewSet.as_view({'post': 'create'}),
        name='infrastructure-habitats-create'
    ),

    # Detalle - Obtiene información detallada de un hábitat de infraestructura
    path(
        '<int:pk>/',
        Habitats_ViewSet.as_view({'get': 'retrieve'}),
        name='infrastructure-habitats-detail'
    ),

    # Actualizar - Modifica un hábitat de infraestructura existente
    path(
        '<int:pk>/update/',
        Habitats_ViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='infrastructure-habitats-update'
    ),

    # Eliminar - Elimina un hábitat de infraestructura
    path(
        '<int:pk>/delete/',
        Habitats_ViewSet.as_view({'delete': 'destroy'}),
        name='infrastructure-habitats-delete'
    ),
]