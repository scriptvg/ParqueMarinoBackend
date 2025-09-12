from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Documento, HistorialDocumento
from .serializers import DocumentoSerializer, HistorialDocumentoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar documentos
    
    Proporciona operaciones CRUD completas para documentos:
    - Listar todos los documentos (GET /api/documentos/)
    - Crear nuevo documento (POST /api/documentos/)
    - Obtener documento específico (GET /api/documentos/{id}/)
    - Actualizar documento (PUT/PATCH /api/documentos/{id}/)
    - Eliminar documento (DELETE /api/documentos/{id}/)
    
    Características:
    - Filtrado por tipo y tags
    - Búsqueda por título y descripción
    - Ordenamiento por fecha
    - Control de permisos por rol
    - Manejo de archivos adjuntos
    
    Ejemplo de uso:
    ```python
    # Crear documento
    POST /api/documentos/
    {"titulo": "Manual de Usuario", "tipo": "MANUAL", "archivo": [file]}
    
    # Actualizar documento
    PATCH /api/documentos/1/
    {"titulo": "Manual de Usuario v2"}
    ```
    """
    
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    
    filterset_fields = ['tipo', 'tags']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def perform_create(self, serializer):
        """
        Asigna el usuario actual como creador del documento
        y registra la creación en el historial.
        """
        documento = serializer.save(creado_por=self.request.user)
        HistorialDocumento.objects.create(
            documento=documento,
            usuario=self.request.user,
            tipo_cambio='CREATE',
            descripcion='Creación inicial del documento'
        )
    
    def perform_update(self, serializer):
        """
        Registra la actualización en el historial del documento.
        """
        documento = serializer.instance
        version_anterior = documento.version
        documento_actualizado = serializer.save()
        
        HistorialDocumento.objects.create(
            documento=documento_actualizado,
            usuario=self.request.user,
            tipo_cambio='UPDATE',
            descripcion='Actualización de documento',
            version_anterior=version_anterior
        )
    
    def perform_destroy(self, instance):
        """
        Registra la eliminación en el historial antes de eliminar el documento.
        """
        HistorialDocumento.objects.create(
            documento=instance,
            usuario=self.request.user,
            tipo_cambio='DELETE',
            descripcion='Eliminación de documento'
        )
        instance.delete()

class HistorialDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar el historial de documentos
    
    Proporciona endpoints de solo lectura para el historial:
    - Listar todo el historial (GET /api/historial/)
    - Obtener entrada específica (GET /api/historial/{id}/)
    
    Características:
    - Filtrado por documento y tipo de cambio
    - Búsqueda por descripción
    - Ordenamiento por fecha
    
    Ejemplo de uso:
    ```python
    # Obtener historial de un documento
    GET /api/historial/?documento=1
    
    # Filtrar por tipo de cambio
    GET /api/historial/?tipo_cambio=UPDATE
    ```
    """
    
    queryset = HistorialDocumento.objects.all()
    serializer_class = HistorialDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filterset_fields = ['documento', 'tipo_cambio', 'usuario']
    search_fields = ['descripcion']
    ordering_fields = ['fecha']
