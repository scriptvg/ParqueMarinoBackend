from django.urls import path
from apps.business.tickets.views import TicketViewSet, VisitViewSet

# Configuración de las rutas para la API de Tickets (Boletos)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'tickets'

urlpatterns = [
    # Tickets - Gestión de tickets del parque
    path('tickets/', TicketViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='tickets-list-create'),
    
    path('tickets/<int:pk>/', TicketViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='tickets-detail'),

    # Visitas - Gestión de visitas programadas
    path('visits/', VisitViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='visits-list-create'),
    
    path('visits/<int:pk>/', VisitViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='visits-detail'),
]