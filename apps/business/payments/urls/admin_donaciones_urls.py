from django.urls import path
from apps.business.payments.views import AdminDonacionViewSet

# Configuración de rutas para el módulo de Administración de Donaciones
# Este módulo maneja toda la lógica administrativa relacionada con las donaciones

app_name = 'admin_donaciones'

urlpatterns = [
    # Listar - Obtiene todas las donaciones (administrador)
    path(
        '',
        AdminDonacionViewSet.as_view({'get': 'list'}),
        name='admin-donaciones-list'
    ),

    # Crear - Añade una nueva donación (administrador)
    path(
        'create/',
        AdminDonacionViewSet.as_view({'post': 'create'}),
        name='admin-donaciones-create'
    ),

    # Detalle - Obtiene información detallada de una donación (administrador)
    path(
        '<int:pk>/',
        AdminDonacionViewSet.as_view({'get': 'retrieve'}),
        name='admin-donaciones-detail'
    ),

    # Actualizar - Modifica una donación existente (administrador)
    path(
        '<int:pk>/update/',
        AdminDonacionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='admin-donaciones-update'
    ),

    # Eliminar - Elimina una donación (administrador)
    path(
        '<int:pk>/delete/',
        AdminDonacionViewSet.as_view({'delete': 'destroy'}),
        name='admin-donaciones-delete'
    ),
]