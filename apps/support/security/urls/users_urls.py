from django.urls import path
from apps.support.security.views import Users_ViewSet

urlpatterns = [
    # Usuarios
    # Ruta para listar
    path('users/', Users_ViewSet.as_view({'get': 'list'}), name='users-get'),
    
    # Ruta para crear
    path('users/create/', Users_ViewSet.as_view({'get': 'list', 'post': 'create'}), name='users-create'),
    
    # Ruta para detalle
    path('users/<int:pk>/detail/', Users_ViewSet.as_view({'get': 'list'}), name='users-detail'),
    
    # Ruta para actualizar o editar
    path('users/<int:pk>/update/', Users_ViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='users-update'),
    
    # Ruta para eliminar
    path('users/<int:pk>/delete/', Users_ViewSet.as_view({'delete': 'destroy'}), name='users-delete'),
]