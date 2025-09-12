from django.urls import path
from apps.business.education.views import HorarioViewSet

# Configuración de rutas para el módulo de Horarios
# Este módulo maneja toda la lógica relacionada con los horarios de los programas

app_name = 'horarios'

urlpatterns = [
    # Listar - Obtiene todos los horarios
    path(
        '',
        HorarioViewSet.as_view({'get': 'list'}),
        name='horarios-list'
    ),

    # Crear - Añade un nuevo horario
    path(
        'create/',
        HorarioViewSet.as_view({'post': 'create'}),
        name='horarios-create'
    ),

    # Detalle - Obtiene información detallada de un horario
    path(
        '<int:pk>/',
        HorarioViewSet.as_view({'get': 'retrieve'}),
        name='horarios-detail'
    ),

    # Actualizar - Modifica un horario existente
    path(
        '<int:pk>/update/',
        HorarioViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='horarios-update'
    ),

    # Eliminar - Elimina un horario
    path(
        '<int:pk>/delete/',
        HorarioViewSet.as_view({'delete': 'destroy'}),
        name='horarios-delete'
    ),
]