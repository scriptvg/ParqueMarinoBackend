from django.test import TestCase, TransactionTestCase, override_settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from datetime import datetime
import os
import tempfile
from unittest.mock import patch, MagicMock

from .models import Documento, HistorialDocumento

User = get_user_model()


from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from unittest.mock import patch, MagicMock

from .models import Documento, HistorialDocumento

User = get_user_model()


class DocumentoModelTest(TestCase):
    """Test suite para el modelo Documento."""
    
    def setUp(self):
        """Configurar datos de prueba para cada método de test."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_creation_basic(self, mock_save):
        """Test creación básica de documento."""
        mock_save.return_value = 'documentos/test_document.pdf'
        
        test_file = SimpleUploadedFile(
            'test_document.pdf',
            b'fake pdf content',
            content_type='application/pdf'
        )
        
        documento = Documento.objects.create(
            titulo='Documento de Prueba',
            tipo='REPORT',
            descripcion='Este es un documento de prueba',
            archivo=test_file,
            creado_por=self.user,
            version='1.0'
        )
        
        self.assertEqual(documento.titulo, 'Documento de Prueba')
        self.assertEqual(documento.tipo, 'REPORT')
        self.assertEqual(documento.creado_por, self.user)
        self.assertEqual(documento.version, '1.0')
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_str_representation(self, mock_save):
        """Test representación string del documento."""
        mock_save.return_value = 'documentos/manual.pdf'
        
        test_file = SimpleUploadedFile('manual.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Manual de Usuario',
            tipo='MANUAL',
            archivo=test_file,
            version='2.1'
        )
        
        expected_str = 'Manual de Usuario - v2.1'
        self.assertEqual(str(documento), expected_str)
        
    def test_documento_tipo_choices_validation(self):
        """Test validación de opciones de tipo."""
        valid_tipos = ['REPORT', 'POLICY', 'MANUAL', 'CONTRACT', 'OTHER']
        
        for tipo in valid_tipos:
            documento = Documento(
                titulo=f'Documento {tipo}',
                tipo=tipo
            )
            # No debería lanzar error de validación
            try:
                documento.full_clean(exclude=['archivo'])
            except ValidationError:
                self.fail(f"Tipo {tipo} no debería ser válido")
                
    def test_documento_default_version(self):
        """Test versión por defecto del documento."""
        documento = Documento(
            titulo='Documento Sin Versión',
            tipo='OTHER'
        )
        
        self.assertEqual(documento.version, '1.0')
        
    def test_documento_titulo_max_length_validation(self):
        """Test validación de longitud máxima del título."""
        long_title = 'A' * 201  # 201 caracteres, excede max_length=200
        
        documento = Documento(
            titulo=long_title,
            tipo='OTHER'
        )
        
        with self.assertRaises(ValidationError):
            documento.full_clean()
            
    def test_documento_meta_options(self):
        """Test opciones del modelo Meta."""
        # Test verbose names
        meta = Documento._meta
        self.assertEqual(meta.verbose_name, 'Documento')
        self.assertEqual(meta.verbose_name_plural, 'Documentos')
        self.assertEqual(meta.ordering, ['-fecha_modificacion'])
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_relacionado_usuario(self, mock_save):
        """Test relación con usuario creador."""
        mock_save.return_value = 'documentos/test.pdf'
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Documento con Usuario',
            tipo='OTHER',
            archivo=test_file,
            creado_por=self.user
        )
        
        # Test que el related_name funciona
        documentos_usuario = self.user.documentos_creados.all()
        self.assertIn(documento, documentos_usuario)
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_file_processing(self, mock_save):
        """Test procesamiento de archivo en save method."""
        mock_save.return_value = 'documentos/test.pdf'
        
        test_file = SimpleUploadedFile(
            'test.pdf',
            b'fake pdf content' * 100,  # Hacer archivo más grande
            content_type='application/pdf'
        )
        
        documento = Documento.objects.create(
            titulo='Documento con Archivo',
            tipo='REPORT',
            archivo=test_file
        )
        
        # Verificar que se estableció el tipo de archivo
        self.assertEqual(documento.tipo_archivo, 'pdf')
        # Verificar que se calculó el tamaño
        self.assertIsNotNone(documento.tamano_archivo)
        

class HistorialDocumentoModelTest(TestCase):
    """Test suite para el modelo HistorialDocumento."""
    
    def setUp(self):
        """Configurar datos de prueba para cada método de test."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        with patch('documents.models.Documento.archivo.field.storage.save') as mock_save:
            mock_save.return_value = 'documentos/test.pdf'
            
            test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
            
            self.documento = Documento.objects.create(
                titulo='Documento de Prueba',
                tipo='REPORT',
                archivo=test_file,
                creado_por=self.user
            )
        
    def test_historial_documento_creation(self):
        """Test creación básica de historial de documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación inicial del documento'
        )
        
        self.assertEqual(historial.documento, self.documento)
        self.assertEqual(historial.usuario, self.user)
        self.assertEqual(historial.tipo_cambio, 'CREATE')
        self.assertEqual(historial.descripcion, 'Creación inicial del documento')
        
    def test_historial_documento_str_representation(self):
        """Test representación string del historial."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Actualización de contenido'
        )
        
        expected_str = f'{self.documento.titulo} - Actualización - {historial.fecha}'
        self.assertEqual(str(historial), expected_str)
        
    def test_historial_documento_tipo_cambio_choices(self):
        """Test validación de opciones de tipo de cambio."""
        valid_tipos = ['CREATE', 'UPDATE', 'DELETE', 'VERSION']
        
        for tipo in valid_tipos:
            historial = HistorialDocumento(
                documento=self.documento,
                usuario=self.user,
                tipo_cambio=tipo,
                descripcion=f'Cambio tipo {tipo}'
            )
            # No debería lanzar error de validación
            try:
                historial.full_clean()
            except ValidationError:
                self.fail(f"Tipo de cambio {tipo} debería ser válido")
                
    def test_historial_documento_cascade_delete(self):
        """Test eliminación en cascada cuando se elimina documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Historial de prueba'
        )
        
        historial_id = historial.id
        
        # Eliminar el documento
        self.documento.delete()
        
        # El historial debería eliminarse también
        with self.assertRaises(HistorialDocumento.DoesNotExist):
            HistorialDocumento.objects.get(id=historial_id)
            
    def test_historial_documento_user_set_null(self):
        """Test que usuario se establece a NULL cuando se elimina usuario."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Historial de prueba'
        )
        
        # Eliminar el usuario
        self.user.delete()
        
        # Recargar historial
        historial.refresh_from_db()
        
        # El usuario debería ser NULL
        self.assertIsNone(historial.usuario)
        
    def test_historial_documento_meta_options(self):
        """Test opciones del modelo Meta."""
        # Test verbose names
        meta = HistorialDocumento._meta
        self.assertEqual(meta.verbose_name, 'Historial de Documento')
        self.assertEqual(meta.verbose_name_plural, 'Historial de Documentos')
        self.assertEqual(meta.ordering, ['-fecha'])
        
    def test_historial_documento_related_name(self):
        """Test related_name para el campo documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Test related name'
        )
        
        # Test que el related_name 'historial' funciona
        historial_documento = self.documento.historial.all()
        self.assertIn(historial, historial_documento)
        
    def test_historial_documento_multiple_entries(self):
        """Test múltiples entradas de historial para un documento."""
        # Crear múltiples entradas de historial
        historial1 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación'
        )
        
        historial2 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Primera actualización'
        )
        
        historial3 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Segunda actualización'
        )
        
        # Verificar que todas las entradas están relacionadas
        historial_count = self.documento.historial.count()
        self.assertEqual(historial_count, 3)
        
        # Verificar orden (más reciente primero)
        historial_ordenado = self.documento.historial.all()
        self.assertEqual(historial_ordenado[0], historial3)
        self.assertEqual(historial_ordenado[1], historial2)
        self.assertEqual(historial_ordenado[2], historial1)
        
    def test_historial_documento_without_usuario(self):
        """Test creación de historial sin usuario (valor NULL)."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=None,
            tipo_cambio='CREATE',
            descripcion='Historial sin usuario'
        )
        
        self.assertIsNone(historial.usuario)
        
    def test_historial_documento_version_tracking(self):
        """Test seguimiento de versiones en el historial."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='VERSION',
            descripcion='Nueva versión',
            version_anterior='1.0'
        )
        
        self.assertEqual(historial.version_anterior, '1.0')
        self.assertEqual(historial.tipo_cambio, 'VERSION')
        
    def test_documento_tipo_choices(self):
        """Test validación de opciones de tipo."""
        valid_tipos = ['REPORT', 'POLICY', 'MANUAL', 'CONTRACT', 'OTHER']
        
        for tipo in valid_tipos:
            documento = Documento(
                titulo=f'Documento {tipo}',
                tipo=tipo,
                archivo=self.test_file
            )
            # No debería lanzar error de validación
            documento.full_clean()
            
    def test_documento_default_version(self):
        """Test versión por defecto del documento."""
        documento = Documento.objects.create(
            titulo='Documento Sin Versión',
            tipo='OTHER',
            archivo=self.test_file
        )
        
        self.assertEqual(documento.version, '1.0')
        
    def test_documento_optional_fields(self):
        """Test campos opcionales del documento."""
        documento = Documento.objects.create(
            titulo='Documento Mínimo',
            tipo='OTHER',
            archivo=self.test_file
        )
        
        self.assertEqual(documento.descripcion, '')
        self.assertIsNone(documento.creado_por)
        self.assertEqual(documento.tags, '')
        
    def test_documento_file_size_calculation(self):
        """Test cálculo automático del tamaño de archivo."""
        # Archivo pequeño (bytes)
        small_file = SimpleUploadedFile(
            'small.txt',
            b'small content',  # 13 bytes
            content_type='text/plain'
        )
        
        documento = Documento.objects.create(
            titulo='Archivo Pequeño',
            tipo='OTHER',
            archivo=small_file
        )
        
        self.assertIn('B', documento.tamano_archivo)
        
    def test_documento_file_type_extraction(self):
        """Test extracción automática del tipo de archivo."""
        pdf_file = SimpleUploadedFile(
            'document.pdf',
            b'pdf content',
            content_type='application/pdf'
        )
        
        documento = Documento.objects.create(
            titulo='Documento PDF',
            tipo='REPORT',
            archivo=pdf_file
        )
        
        self.assertEqual(documento.tipo_archivo, 'pdf')
        
    def test_documento_timestamps(self):
        """Test timestamps automáticos."""
        documento = Documento.objects.create(
            titulo='Documento con Timestamps',
            tipo='OTHER',
            archivo=self.test_file
        )
        
        self.assertIsNotNone(documento.fecha_creacion)
        self.assertIsNotNone(documento.fecha_modificacion)
        
        # La fecha de modificación debería ser igual o posterior a la de creación
        self.assertGreaterEqual(documento.fecha_modificacion, documento.fecha_creacion)
        
    def test_documento_meta_options(self):
        """Test opciones del modelo Meta."""
        documento = Documento.objects.create(
            titulo='Test Meta',
            tipo='OTHER',
            archivo=self.test_file
        )
        
        # Test verbose names
        self.assertEqual(documento._meta.verbose_name, 'Documento')
        self.assertEqual(documento._meta.verbose_name_plural, 'Documentos')
        
        # Test ordering
        self.assertEqual(documento._meta.ordering, ['-fecha_modificacion'])
        
    def test_documento_related_name(self):
        """Test related_name para el campo creado_por."""
        documento = Documento.objects.create(
            titulo='Documento con Usuario',
            tipo='OTHER',
            archivo=self.test_file,
            creado_por=self.user
        )
        
        # Test que el related_name funciona
        documentos_usuario = self.user.documentos_creados.all()
        self.assertIn(documento, documentos_usuario)
        
    def test_documento_without_file(self):
        """Test creación de documento sin archivo."""
        # Esto debería fallar ya que archivo es requerido
        documento = Documento(
            titulo='Documento Sin Archivo',
            tipo='OTHER'
        )
        
        with self.assertRaises(ValidationError):
            documento.full_clean()
            
    def test_documento_titulo_max_length(self):
        """Test validación de longitud máxima del título."""
        long_title = 'A' * 201  # 201 caracteres, excede max_length=200
        
        documento = Documento(
            titulo=long_title,
            tipo='OTHER',
            archivo=self.test_file
        )
        
        with self.assertRaises(ValidationError):
            documento.full_clean()
            
    @patch('documents.models.os.path.splitext')
    def test_documento_file_type_error_handling(self, mock_splitext):
        """Test manejo de errores en extracción de tipo de archivo."""
        # Simular error en splitext
        mock_splitext.side_effect = Exception('Test error')
        
        documento = Documento.objects.create(
            titulo='Documento con Error',
            tipo='OTHER',
            archivo=self.test_file
        )
        
        self.assertEqual(documento.tipo_archivo, 'Desconocido')
        self.assertEqual(documento.tamano_archivo, 'Desconocido')
        

@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class HistorialDocumentoModelTest(TestCase):
    """Test suite para el modelo HistorialDocumento."""
    
    def setUp(self):
        """Configurar datos de prueba para cada método de test."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.test_file = SimpleUploadedFile(
            'test_document.pdf',
            b'fake pdf content',
            content_type='application/pdf'
        )
        
        self.documento = Documento.objects.create(
            titulo='Documento de Prueba',
            tipo='REPORT',
            archivo=self.test_file,
            creado_por=self.user
        )
        
    def test_historial_documento_creation(self):
        """Test creación básica de historial de documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación inicial del documento',
            version_anterior=''
        )
        
        self.assertEqual(historial.documento, self.documento)
        self.assertEqual(historial.usuario, self.user)
        self.assertEqual(historial.tipo_cambio, 'CREATE')
        self.assertEqual(historial.descripcion, 'Creación inicial del documento')
        self.assertEqual(historial.version_anterior, '')
        
    def test_historial_documento_str_representation(self):
        """Test representación string del historial."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Actualización de contenido'
        )
        
        expected_str = f'{self.documento.titulo} - Actualización - {historial.fecha}'
        self.assertEqual(str(historial), expected_str)
        
    def test_historial_documento_tipo_cambio_choices(self):
        """Test validación de opciones de tipo de cambio."""
        valid_tipos = ['CREATE', 'UPDATE', 'DELETE', 'VERSION']
        
        for tipo in valid_tipos:
            historial = HistorialDocumento(
                documento=self.documento,
                usuario=self.user,
                tipo_cambio=tipo,
                descripcion=f'Cambio tipo {tipo}'
            )
            # No debería lanzar error de validación
            historial.full_clean()
            
    def test_historial_documento_cascade_delete(self):
        """Test eliminación en cascada cuando se elimina documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Historial de prueba'
        )
        
        historial_id = historial.id
        
        # Eliminar el documento
        self.documento.delete()
        
        # El historial debería eliminarse también
        with self.assertRaises(HistorialDocumento.DoesNotExist):
            HistorialDocumento.objects.get(id=historial_id)
            
    def test_historial_documento_user_set_null(self):
        """Test que usuario se establece a NULL cuando se elimina usuario."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Historial de prueba'
        )
        
        # Eliminar el usuario
        self.user.delete()
        
        # Recargar historial
        historial.refresh_from_db()
        
        # El usuario debería ser NULL
        self.assertIsNone(historial.usuario)
        
    def test_historial_documento_timestamps(self):
        """Test timestamp automático de fecha."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Test timestamp'
        )
        
        self.assertIsNotNone(historial.fecha)
        
    def test_historial_documento_meta_options(self):
        """Test opciones del modelo Meta."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Test meta'
        )
        
        # Test verbose names
        self.assertEqual(historial._meta.verbose_name, 'Historial de Documento')
        self.assertEqual(historial._meta.verbose_name_plural, 'Historial de Documentos')
        
        # Test ordering
        self.assertEqual(historial._meta.ordering, ['-fecha'])
        
    def test_historial_documento_related_name(self):
        """Test related_name para el campo documento."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Test related name'
        )
        
        # Test que el related_name 'historial' funciona
        historial_documento = self.documento.historial.all()
        self.assertIn(historial, historial_documento)
        
    def test_historial_documento_multiple_entries(self):
        """Test múltiples entradas de historial para un documento."""
        # Crear múltiples entradas de historial
        historial1 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación'
        )
        
        historial2 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Primera actualización'
        )
        
        historial3 = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='UPDATE',
            descripcion='Segunda actualización'
        )
        
        # Verificar que todas las entradas están relacionadas
        historial_count = self.documento.historial.count()
        self.assertEqual(historial_count, 3)
        
        # Verificar orden (más reciente primero)
        historial_ordenado = self.documento.historial.all()
        self.assertEqual(historial_ordenado[0], historial3)
        self.assertEqual(historial_ordenado[1], historial2)
        self.assertEqual(historial_ordenado[2], historial1)
        
    def test_historial_documento_without_usuario(self):
        """Test creación de historial sin usuario (valor NULL)."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=None,
            tipo_cambio='CREATE',
            descripcion='Historial sin usuario'
        )
        
        self.assertIsNone(historial.usuario)
        
    def test_historial_documento_version_tracking(self):
        """Test seguimiento de versiones en el historial."""
        historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='VERSION',
            descripcion='Nueva versión',
            version_anterior='1.0'
        )
        
        self.assertEqual(historial.version_anterior, '1.0')
        self.assertEqual(historial.tipo_cambio, 'VERSION')
