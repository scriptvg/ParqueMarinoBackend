from django.urls import path
from apps.business.education.views import InscripcionViewSet

# Configuración de rutas para el módulo de Inscripciones
# Este módulo maneja toda la lógica relacionada con las inscripciones a programas

app_name = 'inscripciones'

urlpatterns = [
    # Listar - Obtiene todas las inscripciones
    path(
        '',
        InscripcionViewSet.as_view({'get': 'list'}),
        name='inscripciones-list'
    ),

    # Crear - Añade una nueva inscripción
    path(
        'create/',
        InscripcionViewSet.as_view({'post': 'create'}),
        name='inscripciones-create'
    ),

    # Detalle - Obtiene información detallada de una inscripción
    path(
        '<int:pk>/',
        InscripcionViewSet.as_view({'get': 'retrieve'}),
        name='inscripciones-detail'
    ),

    # Actualizar - Modifica una inscripción existente
    path(
        '<int:pk>/update/',
        InscripcionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='inscripciones-update'
    ),

    # Eliminar - Elimina una inscripción
    path(
        '<int:pk>/delete/',
        InscripcionViewSet.as_view({'delete': 'destroy'}),
        name='inscripciones-delete'
    ),
]