from rest_framework import serializers
from .models import Documento, HistorialDocumento

class DocumentoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Documento
    
    Permite la serialización y deserialización de documentos, incluyendo:
    - Conversión de modelos a JSON y viceversa
    - Validación de datos
    - Manejo de archivos adjuntos
    - Cálculo automático de tipo y tamaño de archivo
    
    Ejemplo de uso:
    ```python
    # Serializar un documento
    documento = Documento.objects.get(id=1)
    serializer = DocumentoSerializer(documento)
    data = serializer.data
    
    # Crear un nuevo documento
    serializer = DocumentoSerializer(data=request.data)
    if serializer.is_valid():
        documento = serializer.save(creado_por=request.user)
    ```
    """
    
    url_archivo = serializers.SerializerMethodField()
    tipo_archivo = serializers.CharField(read_only=True)
    tamano_archivo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Documento
        fields = [
            'id',
            'titulo',
            'tipo',
            'descripcion',
            'archivo',
            'url_archivo',
            'tipo_archivo',
            'tamano_archivo',
            'fecha_creacion',
            'fecha_modificacion',
            'creado_por',
            'version',
            'tags'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion', 'creado_por', 'tipo_archivo', 'tamano_archivo']
    
    def get_url_archivo(self, obj):
        request = self.context.get('request')
        if obj.archivo and request:
            return request.build_absolute_uri(obj.archivo.url)
        return obj.archivo.url if obj.archivo else None

class HistorialDocumentoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo HistorialDocumento
    
    Gestiona la serialización del historial de cambios en documentos:
    - Registro de modificaciones
    - Trazabilidad de cambios
    - Información del usuario que realizó el cambio
    
    Ejemplo de uso:
    ```python
    # Registrar un cambio en el historial
    data = {
        'documento': documento.id,
        'tipo_cambio': 'UPDATE',
        'descripcion': 'Actualización de contenido'
    }
    serializer = HistorialDocumentoSerializer(data=data)
    if serializer.is_valid():
        historial = serializer.save(usuario=request.user)
    ```
    """
    
    class Meta:
        model = HistorialDocumento
        fields = '__all__'
        read_only_fields = ['fecha', 'usuario']