from django.urls import path
from apps.support.audit.views import AuditLogViewSet

# Configuración de las rutas para la API de Audit (Auditoría)
# Cada ruta proporciona endpoints para operaciones de lectura en registros de auditoría

app_name = 'audit'

urlpatterns = [
    # Logs de Auditoría - Gestión de registros de auditoría
    path('logs/', AuditLogViewSet.as_view({
        'get': 'list'
    }), name='audit-logs-list'),
    
    path('logs/<int:pk>/', AuditLogViewSet.as_view({
        'get': 'retrieve'
    }), name='audit-logs-detail'),
]