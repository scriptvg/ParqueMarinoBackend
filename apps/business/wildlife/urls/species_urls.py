from django.urls import path
from apps.business.wildlife.views import SpecieViewSet

# =============================================================================
# ESPECIES MARINAS - CONFIGURACIÓN DE RUTAS
# =============================================================================
# Este módulo gestiona el catálogo de especies marinas del parque,
# incluyendo taxonomía, características biológicas y datos de conservación.
#
# Endpoints disponibles:
# GET    /                    → Listar todas las especies
# POST   /create                    → Registrar nueva especie
# GET    /{id}/detail               → Obtener especie específica
# PUT    /{id}/update               → Actualizar especie completa
# PATCH  /{id}/patch               → Actualizar especie parcial
# DELETE /{id}/delete               → Eliminar especie
# =============================================================================

app_name = 'species'

urlpatterns = [
    # Listar - Obtiene todas las especies
    path(
        '',
        SpecieViewSet.as_view({'get': 'list'}),
        name='species-list'
    ),

    # Crear - Añade una nueva especie
    path(
        'create/',
        SpecieViewSet.as_view({'post': 'create'}),
        name='species-create'
    ),

    # Detalle - Obtiene información detallada de una especie
    path(
        '<int:pk>/',
        SpecieViewSet.as_view({'get': 'retrieve'}),
        name='species-detail'
    ),

    # Actualizar - Modifica una especie existente
    path(
        '<int:pk>/update/',
        SpecieViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='species-update'
    ),

    # Eliminar - Elimina una especie
    path(
        '<int:pk>/delete/',
        SpecieViewSet.as_view({'delete': 'destroy'}),
        name='species-delete'
    ),
]
