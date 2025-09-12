from django.urls import path
from apps.business.payments.views import AdminPagoInscripcionViewSet

# Configuración de rutas para el módulo de Administración de Pagos de Inscripción
# Este módulo maneja toda la lógica administrativa relacionada con los pagos de inscripciones

app_name = 'admin_pagos_inscripcion'

urlpatterns = [
    # Listar - Obtiene todos los pagos de inscripción (administrador)
    path(
        '',
        AdminPagoInscripcionViewSet.as_view({'get': 'list'}),
        name='admin-pagos-inscripcion-list'
    ),

    # Crear - Añade un nuevo pago de inscripción (administrador)
    path(
        'create/',
        AdminPagoInscripcionViewSet.as_view({'post': 'create'}),
        name='admin-pagos-inscripcion-create'
    ),

    # Detalle - Obtiene información detallada de un pago de inscripción (administrador)
    path(
        '<int:pk>/',
        AdminPagoInscripcionViewSet.as_view({'get': 'retrieve'}),
        name='admin-pagos-inscripcion-detail'
    ),

    # Actualizar - Modifica un pago de inscripción existente (administrador)
    path(
        '<int:pk>/update/',
        AdminPagoInscripcionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='admin-pagos-inscripcion-update'
    ),

    # Eliminar - Elimina un pago de inscripción (administrador)
    path(
        '<int:pk>/delete/',
        AdminPagoInscripcionViewSet.as_view({'delete': 'destroy'}),
        name='admin-pagos-inscripcion-delete'
    ),
]