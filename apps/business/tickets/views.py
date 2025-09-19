from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from .models import Ticket, Visit
from .serializers import TicketSerializer, VisitSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar tickets.
    
    Proporciona operaciones CRUD para tickets y endpoints adicionales para
    verificar disponibilidad.
    
    Attributes:
        queryset: Conjunto de tickets
        serializer_class: Clase serializadora para tickets
        permission_classes: Permisos requeridos para acceder a las vistas
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        """Define permisos según la acción.
        
        Los administradores pueden realizar todas las operaciones.
        Los usuarios autenticados solo pueden ver tickets.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny] # Allow public read
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """Verifica la disponibilidad de cupos para un ticket.
        
        Args:
            request: Solicitud HTTP con la cantidad de cupos requeridos
            pk: ID del ticket
            
        Returns:
            Response: Respuesta con la disponibilidad de cupos
        """
        ticket = self.get_object()
        slots = request.data.get('slots', 1)

        if not isinstance(slots, int) or slots <= 0:
            return Response(
                {"error": "La cantidad de cupos debe ser un número positivo"},
                status=status.HTTP_400_BAD_REQUEST
            )

        available = ticket.has_available_slots(slots)
        return Response({
            "available": available,
            "requested_slots": slots,
            "available_slots": ticket.total_slots - ticket.occupied_slots
        })

class VisitViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar visitas.
    
    Proporciona operaciones CRUD para visitas y endpoints adicionales para
    verificar disponibilidad.
    
    Attributes:
        queryset: Conjunto de visitas
        serializer_class: Clase serializadora para visitas
        permission_classes: Permisos requeridos para acceder a las vistas
    """
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def get_permissions(self):
        """Define permisos según la acción.
        
        Los administradores pueden realizar todas las operaciones.
        Los usuarios autenticados solo pueden ver visitas.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def available_dates(self, request):
        """Lista las fechas disponibles para visitas.
        
        Returns:
            Response: Lista de fechas con cupos disponibles
        """
        today = timezone.now().date()
        visits = Visit.objects.filter(day__gte=today)
        
        available_visits = []
        for visit in visits:
            if visit.total_slots > visit.occupied_slots:
                serializer = self.get_serializer(visit)
                available_visits.append(serializer.data)
        
        return Response(available_visits)

    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """Verifica la disponibilidad de cupos para una fecha.
        
        Args:
            request: Solicitud HTTP con la cantidad de cupos requeridos
            pk: ID de la visita
            
        Returns:
            Response: Respuesta con la disponibilidad de cupos
        """
        visit = self.get_object()
        slots = request.data.get('slots', 1)

        if not isinstance(slots, int) or slots <= 0:
            return Response(
                {"error": "La cantidad de cupos debe ser un número positivo"},
                status=status.HTTP_400_BAD_REQUEST
            )

        available = visit.has_available_slots(slots)
        return Response({
            "available": available,
            "requested_slots": slots,
            "available_slots": visit.total_slots - visit.occupied_slots
        })
