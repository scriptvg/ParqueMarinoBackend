from django.urls import path
from apps.business.education.views import InstructorViewSet

# Configuración de rutas para el módulo de Instructores
# Este módulo maneja toda la lógica relacionada con los instructores del parque

app_name = 'instructores'

urlpatterns = [
    # Listar - Obtiene todos los instructores
    path(
        '',
        InstructorViewSet.as_view({'get': 'list'}),
        name='instructores-list'
    ),

    # Crear - Añade un nuevo instructor
    path(
        'create/',
        InstructorViewSet.as_view({'post': 'create'}),
        name='instructores-create'
    ),

    # Detalle - Obtiene información detallada de un instructor
    path(
        '<int:pk>/',
        InstructorViewSet.as_view({'get': 'retrieve'}),
        name='instructores-detail'
    ),

    # Actualizar - Modifica un instructor existente
    path(
        '<int:pk>/update/',
        InstructorViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='instructores-update'
    ),

    # Eliminar - Elimina un instructor
    path(
        '<int:pk>/delete/',
        InstructorViewSet.as_view({'delete': 'destroy'}),
        name='instructores-delete'
    ),
]