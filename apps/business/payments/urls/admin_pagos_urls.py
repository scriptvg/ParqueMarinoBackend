from django.urls import path
from apps.business.payments.views import AdminPagoViewSet

# Configuración de rutas para el módulo de Administración de Pagos
# Este módulo maneja toda la lógica administrativa relacionada con los pagos

app_name = 'admin_pagos'

urlpatterns = [
    # Listar - Obtiene todos los pagos (administrador)
    path(
        '',
        AdminPagoViewSet.as_view({'get': 'list'}),
        name='admin-pagos-list'
    ),

    # Crear - Añade un nuevo pago (administrador)
    path(
        'create/',
        AdminPagoViewSet.as_view({'post': 'create'}),
        name='admin-pagos-create'
    ),

    # Detalle - Obtiene información detallada de un pago (administrador)
    path(
        '<int:pk>/',
        AdminPagoViewSet.as_view({'get': 'retrieve'}),
        name='admin-pagos-detail'
    ),

    # Actualizar - Modifica un pago existente (administrador)
    path(
        '<int:pk>/update/',
        AdminPagoViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='admin-pagos-update'
    ),

    # Eliminar - Elimina un pago (administrador)
    path(
        '<int:pk>/delete/',
        AdminPagoViewSet.as_view({'delete': 'destroy'}),
        name='admin-pagos-delete'
    ),
]