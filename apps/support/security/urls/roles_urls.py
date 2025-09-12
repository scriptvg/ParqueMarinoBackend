from django.urls import path
from apps.support.security.views import GroupViewSet

urlpatterns = [
    # Roles
    # Ruta para listar
    path('roles/', GroupViewSet.as_view({'get': 'list'}), name='roles-get'),

    # Ruta para crear
    path('roles/create/', GroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='roles-create'),

    # Ruta para detalle
    path('roles/<int:pk>/detail/', GroupViewSet.as_view({'get': 'list'}), name='roles-detail'),

    # Ruta para actualizar o editar
    path('roles/<int:pk>/update/', GroupViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='roles-update'),

    # Ruta para eliminar
    path('roles/<int:pk>/delete/', GroupViewSet.as_view({'delete': 'destroy'}), name='roles-delete'),
]