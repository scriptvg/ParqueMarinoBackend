from django.urls import path
from apps.business.payments.views import DonacionViewSet

# Configuración de rutas para el módulo de Donaciones
# Este módulo maneja toda la lógica relacionada con las donaciones al parque

app_name = 'donaciones'

urlpatterns = [
    # Listar - Obtiene todas las donaciones
    path(
        '',
        DonacionViewSet.as_view({'get': 'list'}),
        name='donaciones-list'
    ),

    # Crear - Añade una nueva donación
    path(
        'create/',
        DonacionViewSet.as_view({'post': 'create'}),
        name='donaciones-create'
    ),

    # Detalle - Obtiene información detallada de una donación
    path(
        '<int:pk>/',
        DonacionViewSet.as_view({'get': 'retrieve'}),
        name='donaciones-detail'
    ),

    # Procesar donación - Procesa una donación
    path(
        '<int:pk>/procesar_donacion/',
        DonacionViewSet.as_view({'post': 'procesar_donacion'}),
        name='donaciones-procesar-donacion'
    ),
    
    # Procesar pago - Procesa una donación con Stripe
    path(
        '<int:pk>/procesar_pago/',
        DonacionViewSet.as_view({'post': 'procesar_pago'}),
        name='donaciones-procesar-pago'
    ),

    # Actualizar - Modifica una donación existente
    path(
        '<int:pk>/update/',
        DonacionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='donaciones-update'
    ),

    # Eliminar - Elimina una donación
    path(
        '<int:pk>/delete/',
        DonacionViewSet.as_view({'delete': 'destroy'}),
        name='donaciones-delete'
    ),
]