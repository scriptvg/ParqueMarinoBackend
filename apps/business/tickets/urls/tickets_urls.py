from django.urls import path
from apps.business.tickets.views import TicketViewSet

# Configuración de rutas para el módulo de Tickets
# Este módulo maneja toda la lógica relacionada con los tickets del parque

app_name = 'tickets'

urlpatterns = [
    # Listar - Obtiene todos los tickets
    path(
        '',
        TicketViewSet.as_view({'get': 'list'}),
        name='tickets-list'
    ),

    # Crear - Añade un nuevo ticket
    path(
        'create/',
        TicketViewSet.as_view({'post': 'create'}),
        name='tickets-create'
    ),

    # Detalle - Obtiene información detallada de un ticket
    path(
        '<int:pk>/',
        TicketViewSet.as_view({'get': 'retrieve'}),
        name='tickets-detail'
    ),

    # Verificar disponibilidad - Verifica la disponibilidad de cupos para un ticket
    path(
        '<int:pk>/check_availability/',
        TicketViewSet.as_view({'post': 'check_availability'}),
        name='tickets-check-availability'
    ),

    # Actualizar - Modifica un ticket existente
    path(
        '<int:pk>/update/',
        TicketViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='tickets-update'
    ),

    # Eliminar - Elimina un ticket
    path(
        '<int:pk>/delete/',
        TicketViewSet.as_view({'delete': 'destroy'}),
        name='tickets-delete'
    ),
]