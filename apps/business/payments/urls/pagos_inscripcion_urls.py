from django.urls import path
from apps.business.payments.views import PagoInscripcionViewSet

# Configuración de rutas para el módulo de Pagos de Inscripción
# Este módulo maneja toda la lógica relacionada con los pagos de inscripciones

app_name = 'pagos_inscripcion'

urlpatterns = [
    # Listar - Obtiene todos los pagos de inscripción
    path(
        '',
        PagoInscripcionViewSet.as_view({'get': 'list'}),
        name='pagos-inscripcion-list'
    ),

    # Crear - Añade un nuevo pago de inscripción
    path(
        'create/',
        PagoInscripcionViewSet.as_view({'post': 'create'}),
        name='pagos-inscripcion-create'
    ),

    # Detalle - Obtiene información detallada de un pago de inscripción
    path(
        '<int:pk>/',
        PagoInscripcionViewSet.as_view({'get': 'retrieve'}),
        name='pagos-inscripcion-detail'
    ),

    # Procesar pago - Procesa el pago de una inscripción
    path(
        '<int:pk>/procesar_pago/',
        PagoInscripcionViewSet.as_view({'post': 'procesar_pago'}),
        name='pagos-inscripcion-procesar'
    ),

    # Actualizar - Modifica un pago de inscripción existente
    path(
        '<int:pk>/update/',
        PagoInscripcionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='pagos-inscripcion-update'
    ),

    # Eliminar - Elimina un pago de inscripción
    path(
        '<int:pk>/delete/',
        PagoInscripcionViewSet.as_view({'delete': 'destroy'}),
        name='pagos-inscripcion-delete'
    ),
]