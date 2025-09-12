from django.urls import path
from apps.business.payments.views import PagoViewSet

# Configuración de rutas para el módulo de Pagos
# Este módulo maneja toda la lógica relacionada con los pagos generales

app_name = 'pagos'

urlpatterns = [
    # Listar - Obtiene todos los pagos
    path(
        '',
        PagoViewSet.as_view({'get': 'list'}),
        name='pagos-list'
    ),

    # Crear - Añade un nuevo pago
    path(
        'create/',
        PagoViewSet.as_view({'post': 'create'}),
        name='pagos-create'
    ),

    # Detalle - Obtiene información detallada de un pago
    path(
        '<int:pk>/',
        PagoViewSet.as_view({'get': 'retrieve'}),
        name='pagos-detail'
    ),
    
    # Procesar pago - Procesa un pago general con Stripe
    path(
        '<int:pk>/procesar_pago/',
        PagoViewSet.as_view({'post': 'procesar_pago'}),
        name='pagos-procesar'
    ),

    # Actualizar - Modifica un pago existente
    path(
        '<int:pk>/update/',
        PagoViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='pagos-update'
    ),

    # Eliminar - Elimina un pago
    path(
        '<int:pk>/delete/',
        PagoViewSet.as_view({'delete': 'destroy'}),
        name='pagos-delete'
    ),
]