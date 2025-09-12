from django.urls import path
from apps.business.tickets.views import VisitViewSet

# Configuración de rutas para el módulo de Visitas
# Este módulo maneja toda la lógica relacionada con las visitas al parque

app_name = 'visits'

urlpatterns = [
    # Listar - Obtiene todas las visitas
    path(
        '',
        VisitViewSet.as_view({'get': 'list'}),
        name='visits-list'
    ),

    # Fechas disponibles - Lista las fechas disponibles para visitas
    path(
        'available_dates/',
        VisitViewSet.as_view({'get': 'available_dates'}),
        name='visits-available-dates'
    ),

    # Crear - Añade una nueva visita
    path(
        'create/',
        VisitViewSet.as_view({'post': 'create'}),
        name='visits-create'
    ),

    # Detalle - Obtiene información detallada de una visita
    path(
        '<int:pk>/',
        VisitViewSet.as_view({'get': 'retrieve'}),
        name='visits-detail'
    ),

    # Verificar disponibilidad - Verifica la disponibilidad de cupos para una fecha
    path(
        '<int:pk>/check_availability/',
        VisitViewSet.as_view({'post': 'check_availability'}),
        name='visits-check-availability'
    ),

    # Actualizar - Modifica una visita existente
    path(
        '<int:pk>/update/',
        VisitViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='visits-update'
    ),

    # Eliminar - Elimina una visita
    path(
        '<int:pk>/delete/',
        VisitViewSet.as_view({'delete': 'destroy'}),
        name='visits-delete'
    ),
]