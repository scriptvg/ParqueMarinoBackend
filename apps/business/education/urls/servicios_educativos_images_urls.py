from django.urls import path
from apps.business.education.views import ServiciosEducativosImageViewSet

# Configuración de rutas para el módulo de Imágenes de Servicios Educativos
# Este módulo maneja toda la lógica relacionada con las imágenes de servicios educativos

app_name = 'servicios_educativos_images'

urlpatterns = [
    # Listar - Obtiene todas las imágenes de servicios educativos
    path(
        '',
        ServiciosEducativosImageViewSet.as_view({'get': 'list'}),
        name='servicios-educativos-images-list'
    ),

    # Crear - Añade una nueva imagen de servicio educativo
    path(
        'create/',
        ServiciosEducativosImageViewSet.as_view({'post': 'create'}),
        name='servicios-educativos-images-create'
    ),

    # Detalle - Obtiene información detallada de una imagen de servicio educativo
    path(
        '<int:pk>/',
        ServiciosEducativosImageViewSet.as_view({'get': 'retrieve'}),
        name='servicios-educativos-images-detail'
    ),

    # Actualizar - Modifica una imagen de servicio educativo existente
    path(
        '<int:pk>/update/',
        ServiciosEducativosImageViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='servicios-educativos-images-update'
    ),

    # Eliminar - Elimina una imagen de servicio educativo
    path(
        '<int:pk>/delete/',
        ServiciosEducativosImageViewSet.as_view({'delete': 'destroy'}),
        name='servicios-educativos-images-delete'
    ),
]