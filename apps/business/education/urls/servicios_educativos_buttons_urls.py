from django.urls import path
from apps.business.education.views import ServiciosEducativosButtonsViewSet

# Configuración de rutas para el módulo de Botones de Servicios Educativos
# Este módulo maneja toda la lógica relacionada con los botones de servicios educativos

app_name = 'servicios_educativos_buttons'

urlpatterns = [
    # Listar - Obtiene todos los botones de servicios educativos
    path(
        '',
        ServiciosEducativosButtonsViewSet.as_view({'get': 'list'}),
        name='servicios-educativos-buttons-list'
    ),

    # Crear - Añade un nuevo botón de servicio educativo
    path(
        'create/',
        ServiciosEducativosButtonsViewSet.as_view({'post': 'create'}),
        name='servicios-educativos-buttons-create'
    ),

    # Detalle - Obtiene información detallada de un botón de servicio educativo
    path(
        '<int:pk>/',
        ServiciosEducativosButtonsViewSet.as_view({'get': 'retrieve'}),
        name='servicios-educativos-buttons-detail'
    ),

    # Actualizar - Modifica un botón de servicio educativo existente
    path(
        '<int:pk>/update/',
        ServiciosEducativosButtonsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='servicios-educativos-buttons-update'
    ),

    # Eliminar - Elimina un botón de servicio educativo
    path(
        '<int:pk>/delete/',
        ServiciosEducativosButtonsViewSet.as_view({'delete': 'destroy'}),
        name='servicios-educativos-buttons-delete'
    ),
]