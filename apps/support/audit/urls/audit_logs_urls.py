from django.urls import path
from apps.support.audit.views import AuditLogViewSet

# Configuración de rutas para el módulo de Logs de Auditoría
# Este módulo maneja toda la lógica relacionada con los registros de auditoría del sistema

app_name = 'audit_logs'

urlpatterns = [
    # Listar - Obtiene todos los logs de auditoría
    path(
        '',
        AuditLogViewSet.as_view({'get': 'list'}),
        name='audit-logs-list'
    ),

    # Detalle - Obtiene información detallada de un log de auditoría
    path(
        '<int:pk>/',
        AuditLogViewSet.as_view({'get': 'retrieve'}),
        name='audit-logs-detail'
    ),
]