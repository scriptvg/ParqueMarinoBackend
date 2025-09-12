from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.support.security.permissions import IsAuthenticatedAndRole

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para gestionar los registros de auditoría.
    
    Este ViewSet proporciona endpoints de solo lectura para consultar
    y filtrar los registros de auditoría del sistema.
    
    Attributes:
        queryset: Conjunto de registros de auditoría ordenados por fecha.
        serializer_class: Clase serializadora para los registros.
        permission_classes: Permisos requeridos para acceder a los endpoints.
        filter_backends: Backends para filtrado y búsqueda.
        filterset_fields: Campos por los que se puede filtrar.
        search_fields: Campos en los que se puede buscar.
        ordering_fields: Campos por los que se puede ordenar.
    """
    
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticatedAndRole]
    required_role = 'admin'
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    filterset_fields = {
        'timestamp': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'user': ['exact'],
        'action': ['exact', 'icontains'],
        'model': ['exact', 'icontains'],
        'record_id': ['exact']
    }
    
    search_fields = ['action', 'model', 'details']
    ordering_fields = ['timestamp', 'user', 'action', 'model']
    
    def get_queryset(self):
        """Personaliza el queryset según el usuario.
        
        Si el usuario es staff, puede ver todos los registros.
        Si no, solo puede ver los registros relacionados con él.
        
        Returns:
            QuerySet: Registros de auditoría filtrados según el usuario.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
