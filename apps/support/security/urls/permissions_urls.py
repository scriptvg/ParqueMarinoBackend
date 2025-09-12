from django.urls import path
from apps.support.security.views import GroupPermissionsViewSet

urlpatterns = [
    # Permissions
    # Ruta para listar
    path('permissions/', GroupPermissionsViewSet.as_view({'get': 'list'}), name='permissions-get'),

    # Ruta para crear
    path('permissions/<int:pk>/create/', GroupPermissionsViewSet.as_view({'get': 'list', 'post': 'create'}), name='permissions-create'),

    # Ruta para detalle
    path('permissions/<int:pk>/detail/', GroupPermissionsViewSet.as_view({'get': 'list'}), name='permissions-detail'),

    # Ruta para actualizar o editar
    path('permissions/<int:pk>/update/', GroupPermissionsViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='permissions-update'),

    # Ruta para eliminar
    path('permissions/<int:pk>/delete/', GroupPermissionsViewSet.as_view({'delete': 'destroy'}), name='permissions-delete'),
]