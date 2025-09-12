from django.urls import path
from apps.business.education.views import ServiciosEducativosFactsViewSet

# Configuración de rutas para el módulo de Datos de Servicios Educativos
# Este módulo maneja toda la lógica relacionada con los datos de servicios educativos

app_name = 'servicios_educativos_facts'

urlpatterns = [
    # Listar - Obtiene todos los datos de servicios educativos
    path(
        '',
        ServiciosEducativosFactsViewSet.as_view({'get': 'list'}),
        name='servicios-educativos-facts-list'
    ),

    # Crear - Añade un nuevo dato de servicio educativo
    path(
        'create/',
        ServiciosEducativosFactsViewSet.as_view({'post': 'create'}),
        name='servicios-educativos-facts-create'
    ),

    # Detalle - Obtiene información detallada de un dato de servicio educativo
    path(
        '<int:pk>/',
        ServiciosEducativosFactsViewSet.as_view({'get': 'retrieve'}),
        name='servicios-educativos-facts-detail'
    ),

    # Actualizar - Modifica un dato de servicio educativo existente
    path(
        '<int:pk>/update/',
        ServiciosEducativosFactsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='servicios-educativos-facts-update'
    ),

    # Eliminar - Elimina un dato de servicio educativo
    path(
        '<int:pk>/delete/',
        ServiciosEducativosFactsViewSet.as_view({'delete': 'destroy'}),
        name='servicios-educativos-facts-delete'
    ),
]