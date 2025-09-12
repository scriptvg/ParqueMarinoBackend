from django.urls import path
from apps.business.education.views import ServiciosEducativosDescriptionViewSet

# Configuración de rutas para el módulo de Descripciones de Servicios Educativos
# Este módulo maneja toda la lógica relacionada con las descripciones de servicios educativos

app_name = 'servicios_educativos_descriptions'

urlpatterns = [
    # Listar - Obtiene todas las descripciones de servicios educativos
    path(
        '',
        ServiciosEducativosDescriptionViewSet.as_view({'get': 'list'}),
        name='servicios-educativos-descriptions-list'
    ),

    # Crear - Añade una nueva descripción de servicio educativo
    path(
        'create/',
        ServiciosEducativosDescriptionViewSet.as_view({'post': 'create'}),
        name='servicios-educativos-descriptions-create'
    ),

    # Detalle - Obtiene información detallada de una descripción de servicio educativo
    path(
        '<int:pk>/',
        ServiciosEducativosDescriptionViewSet.as_view({'get': 'retrieve'}),
        name='servicios-educativos-descriptions-detail'
    ),

    # Actualizar - Modifica una descripción de servicio educativo existente
    path(
        '<int:pk>/update/',
        ServiciosEducativosDescriptionViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='servicios-educativos-descriptions-update'
    ),

    # Eliminar - Elimina una descripción de servicio educativo
    path(
        '<int:pk>/delete/',
        ServiciosEducativosDescriptionViewSet.as_view({'delete': 'destroy'}),
        name='servicios-educativos-descriptions-delete'
    ),
]