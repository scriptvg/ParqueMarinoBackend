from django.urls import path
from apps.business.education.views import ServiciosEducativosViewSet

# Configuración de rutas para el módulo de Servicios Educativos
# Este módulo maneja toda la lógica relacionada con los servicios educativos del parque

app_name = 'servicios_educativos'

urlpatterns = [
    # Listar - Obtiene todos los servicios educativos
    path(
        '',
        ServiciosEducativosViewSet.as_view({'get': 'list'}),
        name='servicios-educativos-list'
    ),

    # Crear - Añade un nuevo servicio educativo
    path(
        'create/',
        ServiciosEducativosViewSet.as_view({'post': 'create'}),
        name='servicios-educativos-create'
    ),

    # Detalle - Obtiene información detallada de un servicio educativo
    path(
        '<int:pk>/',
        ServiciosEducativosViewSet.as_view({'get': 'retrieve'}),
        name='servicios-educativos-detail'
    ),

    # Actualizar - Modifica un servicio educativo existente
    path(
        '<int:pk>/update/',
        ServiciosEducativosViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='servicios-educativos-update'
    ),

    # Eliminar - Elimina un servicio educativo
    path(
        '<int:pk>/delete/',
        ServiciosEducativosViewSet.as_view({'delete': 'destroy'}),
        name='servicios-educativos-delete'
    ),
]