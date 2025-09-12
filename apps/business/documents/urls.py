from django.urls import path
from apps.business.documents.views import DocumentoViewSet, HistorialDocumentoViewSet

# Configuración de las rutas para la API de Documents (Documentos)
# Cada ruta proporciona endpoints para operaciones CRUD en diferentes modelos

app_name = 'documents'

urlpatterns = [
    # Documentos - Gestión de documentos del sistema
    path('documentos/', DocumentoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='documentos-list-create'),
    
    path('documentos/<int:pk>/', DocumentoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='documentos-detail'),

    # Historial - Gestión del historial de documentos
    path('historial/', HistorialDocumentoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='historial-documentos-list-create'),
    
    path('historial/<int:pk>/', HistorialDocumentoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='historial-documentos-detail'),
]