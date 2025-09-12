import os
from django.db import models
from django.contrib.auth import get_user_model
from config.storage_backends import MediaStorage

User = get_user_model()

class Documento(models.Model):
    """
    Modelo base para gestionar documentos en el sistema
    
    Este modelo permite almacenar y gestionar diferentes tipos de documentos,
    incluyendo metadatos y el archivo físico. Características principales:
    - Almacenamiento seguro en AWS S3
    - Control de versiones de documentos
    - Seguimiento de cambios y auditoría
    - Categorización y etiquetado
    
    Ejemplo de uso:
    ```python
    documento = Documento.objects.create(
        titulo='Informe Anual 2024',
        tipo='REPORT',
        descripcion='Informe detallado de actividades',
        archivo=request.FILES['documento']
    )
    ```
    
    Para actualizar un documento:
    ```python
    documento.titulo = 'Nuevo título'
    documento.save()
    ```
    """
    
    TIPO_CHOICES = [
        ('REPORT', 'Informe'),
        ('POLICY', 'Política'),
        ('MANUAL', 'Manual'),
        ('CONTRACT', 'Contrato'),
        ('OTHER', 'Otro')
    ]
    
    titulo = models.CharField(
        max_length=200,
        help_text='Título descriptivo del documento'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        help_text='Tipo de documento'
    )
    descripcion = models.TextField(
        blank=True,
        help_text='Descripción detallada del documento'
    )
    archivo = models.FileField(
        upload_to='documentos/',
        storage=MediaStorage(),
        help_text='Archivo del documento'
    )
    tipo_archivo = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='Tipo de archivo (calculado automáticamente)'
    )
    tamano_archivo = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Tamaño del archivo en formato legible'    
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documentos_creados'
    )
    version = models.CharField(
        max_length=50,
        default='1.0',
        help_text='Versión del documento'
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text='Etiquetas separadas por comas'
    )
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_modificacion']
    
    def save(self, *args, **kwargs):
        if self.archivo:
            try:
                # Obtener la extensión del archivo sin el punto (ej. pdf, xlsx)
                extension = os.path.splitext(self.archivo.name)[1].lower()
                self.tipo_archivo = extension[1:] if extension.startswith('.') else extension

                # Calcular tamaño del archivo en formato legible
                size_bytes = self.archivo.size
                if size_bytes < 1024:
                    self.tamano_archivo = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    self.tamano_archivo = f"{size_bytes / 1024:.2f} KB"
                else:
                    self.tamano_archivo = f"{size_bytes / (1024 * 1024):.2f} MB"
            except Exception as e:
                self.tipo_archivo = 'Desconocido'
                self.tamano_archivo = 'Desconocido'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} - v{self.version}'

class HistorialDocumento(models.Model):
    """
    Modelo para registrar el historial de cambios en documentos
    
    Mantiene un registro de todas las modificaciones realizadas a los documentos,
    incluyendo quién realizó el cambio y qué se modificó.
    
    Ejemplo de uso:
    ```python
    historial = HistorialDocumento.objects.create(
        documento=documento,
        usuario=request.user,
        tipo_cambio='UPDATE',
        descripcion='Actualización de contenido'
    )
    ```
    """
    
    TIPO_CAMBIO_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('VERSION', 'Nueva Versión')
    ]
    
    documento = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    tipo_cambio = models.CharField(
        max_length=20,
        choices=TIPO_CAMBIO_CHOICES
    )
    descripcion = models.TextField(
        help_text='Descripción del cambio realizado'
    )
    version_anterior = models.CharField(
        max_length=50,
        blank=True,
        help_text='Versión anterior del documento'
    )
    
    class Meta:
        verbose_name = 'Historial de Documento'
        verbose_name_plural = 'Historial de Documentos'
        ordering = ['-fecha']
    
    def __str__(self):
        return f'{self.documento.titulo} - {self.get_tipo_cambio_display()} - {self.fecha}'
