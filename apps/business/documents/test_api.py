from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.db import transaction
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
import json

from .models import Documento, HistorialDocumento
from .serializers import DocumentoSerializer, HistorialDocumentoSerializer

User = get_user_model()


class DocumentoSerializerTest(TestCase):
    """Test suite para DocumentoSerializer."""
    
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
                descripcion='Descripción del documento',
                archivo=test_file,
                creado_por=self.user,
                version='1.0'
            )
        
    def test_documento_serializer_read(self):
        """Test operaciones de lectura del DocumentoSerializer."""
        serializer = DocumentoSerializer(self.documento)
        data = serializer.data
        
        self.assertEqual(data['titulo'], 'Documento de Prueba')
        self.assertEqual(data['tipo'], 'REPORT')
        self.assertEqual(data['descripcion'], 'Descripción del documento')
        self.assertEqual(data['version'], '1.0')
        self.assertIn('url_archivo', data)
        self.assertIn('tipo_archivo', data)
        self.assertIn('tamano_archivo', data)
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_serializer_create(self, mock_save):
        """Test creación mediante DocumentoSerializer."""
        mock_save.return_value = 'documentos/new_document.pdf'
        
        new_file = SimpleUploadedFile(
            'new_document.pdf',
            b'new pdf content',
            content_type='application/pdf'
        )
        
        data = {
            'titulo': 'Nuevo Documento',
            'tipo': 'MANUAL',
            'descripcion': 'Nuevo documento creado via serializer',
            'archivo': new_file,
            'version': '2.0',
            'tags': 'nuevo, test'
        }
        
        serializer = DocumentoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        documento = serializer.save(creado_por=self.user)
        self.assertEqual(documento.titulo, 'Nuevo Documento')
        self.assertEqual(documento.tipo, 'MANUAL')
        self.assertEqual(documento.creado_por, self.user)
        
    def test_documento_serializer_update(self):
        """Test actualización mediante DocumentoSerializer."""
        update_data = {
            'titulo': 'Documento Actualizado',
            'descripcion': 'Descripción actualizada'
        }
        
        serializer = DocumentoSerializer(self.documento, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        documento_actualizado = serializer.save()
        self.assertEqual(documento_actualizado.titulo, 'Documento Actualizado')
        self.assertEqual(documento_actualizado.descripcion, 'Descripción actualizada')
        
    def test_documento_serializer_readonly_fields(self):
        """Test campos de solo lectura del DocumentoSerializer."""
        readonly_data = {
            'creado_por': None,
            'tipo_archivo': 'txt',
            'tamano_archivo': '100 KB'
        }
        
        serializer = DocumentoSerializer(self.documento, data=readonly_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        # Los campos readonly no deberían cambiar
        documento_actualizado = serializer.save()
        self.assertEqual(documento_actualizado.creado_por, self.user)
        
    def test_documento_serializer_validation(self):
        """Test validación del DocumentoSerializer."""
        # Test sin título
        data = {'tipo': 'REPORT'}
        serializer = DocumentoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo', serializer.errors)
        

class HistorialDocumentoSerializerTest(TestCase):
    """Test suite para HistorialDocumentoSerializer."""
    
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
            
        self.historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación inicial'
        )
        
    def test_historial_documento_serializer_read(self):
        """Test operaciones de lectura del HistorialDocumentoSerializer."""
        serializer = HistorialDocumentoSerializer(self.historial)
        data = serializer.data
        
        self.assertEqual(data['documento'], self.documento.id)
        self.assertEqual(data['usuario'], self.user.id)
        self.assertEqual(data['tipo_cambio'], 'CREATE')
        self.assertEqual(data['descripcion'], 'Creación inicial')
        self.assertIn('fecha', data)
        
    def test_historial_documento_serializer_create(self):
        """Test creación mediante HistorialDocumentoSerializer."""
        data = {
            'documento': self.documento.id,
            'tipo_cambio': 'UPDATE',
            'descripcion': 'Actualización de documento',
            'version_anterior': '1.0'
        }
        
        serializer = HistorialDocumentoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        historial = serializer.save(usuario=self.user)
        self.assertEqual(historial.tipo_cambio, 'UPDATE')
        self.assertEqual(historial.usuario, self.user)
        

class DocumentsAPITestCase(APITestCase):
    """Test suite para los endpoints de la API de Documents."""
    
    def setUp(self):
        """Configurar datos de prueba y autenticación."""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
        )
        
        with patch('documents.models.Documento.archivo.field.storage.save') as mock_save:
            mock_save.return_value = 'documentos/test.pdf'
            
            test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
            
            self.documento = Documento.objects.create(
                titulo='Documento de Prueba',
                tipo='REPORT',
                descripcion='Documento para testing',
                archivo=test_file,
                creado_por=self.admin_user,
                version='1.0'
            )
        
        self.client = APIClient()
        
    def authenticate_admin(self):
        """Autenticar como usuario admin."""
        self.client.force_authenticate(user=self.admin_user)
        
    def authenticate_regular(self):
        """Autenticar como usuario regular."""
        self.client.force_authenticate(user=self.regular_user)
        
    def test_documento_list_requires_authentication(self):
        """Test que listar documentos requiere autenticación."""
        url = reverse('documentos:documentos-list')
        
        # Solicitud sin autenticar
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Solicitud autenticada
        self.authenticate_admin()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_create_api(self, mock_save):
        """Test creación de documento via API."""
        mock_save.return_value = 'documentos/new_doc.pdf'
        
        self.authenticate_admin()
        url = reverse('documentos:documentos-create')
        
        new_file = SimpleUploadedFile(
            'new_document.pdf',
            b'new pdf content',
            content_type='application/pdf'
        )
        
        data = {
            'titulo': 'Nuevo Documento API',
            'tipo': 'MANUAL',
            'descripcion': 'Documento creado via API',
            'archivo': new_file,
            'version': '1.0',
            'tags': 'api, test'
        }
        
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el documento se creó
        documento = Documento.objects.get(titulo='Nuevo Documento API')
        self.assertEqual(documento.creado_por, self.admin_user)
        
    def test_documento_detail_view(self):
        """Test vista de detalle de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-detail', kwargs={'pk': self.documento.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['titulo'], 'Documento de Prueba')
        self.assertEqual(data['tipo'], 'REPORT')
        
    def test_documento_update_api(self):
        """Test actualización de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-update', kwargs={'pk': self.documento.pk})
        
        update_data = {
            'titulo': 'Documento Actualizado via API',
            'descripcion': 'Descripción actualizada'
        }
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar actualización
        self.documento.refresh_from_db()
        self.assertEqual(self.documento.titulo, 'Documento Actualizado via API')
        
    def test_documento_delete_api(self):
        """Test eliminación de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-delete', kwargs={'pk': self.documento.pk})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el documento se eliminó
        with self.assertRaises(Documento.DoesNotExist):
            Documento.objects.get(pk=self.documento.pk)
            

class DocumentsBusinessLogicTest(TestCase):
    """Test suite para lógica de negocio de documents."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_version_management(self, mock_save):
        """Test gestión de versiones de documentos."""
        mock_save.return_value = 'documentos/versioned.pdf'
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Documento Versionado',
            tipo='REPORT',
            archivo=test_file,
            version='1.0'
        )
        
        # Crear historial de versión
        HistorialDocumento.objects.create(
            documento=documento,
            usuario=self.user,
            tipo_cambio='VERSION',
            descripcion='Nueva versión',
            version_anterior='1.0'
        )
        
        # Actualizar versión
        documento.version = '2.0'
        documento.save()
        
        self.assertEqual(documento.version, '2.0')
        
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_documento_tags_functionality(self, mock_save):
        """Test funcionalidad de etiquetas."""
        mock_save.return_value = 'documentos/tagged.pdf'
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Documento con Tags',
            tipo='REPORT',
            archivo=test_file,
            tags='importante, urgente, reporte'
        )
        
        self.assertEqual(documento.tags, 'importante, urgente, reporte')
        
        # Test búsqueda por tags
        documentos_importantes = Documento.objects.filter(tags__icontains='importante')
        self.assertIn(documento, documentos_importantes)
        

class DocumentsSignalsTest(TestCase):
    """Test suite para señales de documents."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    @patch('documents.signals.delete_s3_files_from_instance')
    @patch('documents.models.Documento.archivo.field.storage.save')
    def test_delete_document_s3_files_signal(self, mock_save, mock_delete_s3):
        """Test señal de eliminación de archivos S3."""
        mock_save.return_value = 'documentos/to_delete.pdf'
        mock_delete_s3.return_value = {'success': True}
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        documento = Documento.objects.create(
            titulo='Documento para Eliminar',
            tipo='REPORT',
            archivo=test_file,
            creado_por=self.user
        )
        
        # Eliminar documento
        documento.delete()
        
        # Verificar que se llamó la función de eliminación S3
        mock_delete_s3.assert_called_once()
        
    def test_documento_serializer_create(self):
        """Test creación mediante DocumentoSerializer."""
        new_file = SimpleUploadedFile(
            'new_document.pdf',
            b'new pdf content',
            content_type='application/pdf'
        )
        
        data = {
            'titulo': 'Nuevo Documento',
            'tipo': 'MANUAL',
            'descripcion': 'Nuevo documento creado via serializer',
            'archivo': new_file,
            'version': '2.0',
            'tags': 'nuevo, test'
        }
        
        serializer = DocumentoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        documento = serializer.save(creado_por=self.user)
        self.assertEqual(documento.titulo, 'Nuevo Documento')
        self.assertEqual(documento.tipo, 'MANUAL')
        self.assertEqual(documento.creado_por, self.user)
        
    def test_documento_serializer_update(self):
        """Test actualización mediante DocumentoSerializer."""
        update_data = {
            'titulo': 'Documento Actualizado',
            'descripcion': 'Descripción actualizada'
        }
        
        serializer = DocumentoSerializer(self.documento, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        documento_actualizado = serializer.save()
        self.assertEqual(documento_actualizado.titulo, 'Documento Actualizado')
        self.assertEqual(documento_actualizado.descripcion, 'Descripción actualizada')
        
    def test_documento_serializer_readonly_fields(self):
        """Test campos de solo lectura del DocumentoSerializer."""
        readonly_data = {
            'fecha_creacion': '2024-01-01T00:00:00Z',
            'fecha_modificacion': '2024-01-01T00:00:00Z',
            'creado_por': None,
            'tipo_archivo': 'txt',
            'tamano_archivo': '100 KB'
        }
        
        serializer = DocumentoSerializer(self.documento, data=readonly_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        # Los campos readonly no deberían cambiar
        documento_actualizado = serializer.save()
        self.assertEqual(documento_actualizado.creado_por, self.user)
        self.assertNotEqual(documento_actualizado.tipo_archivo, 'txt')
        
    def test_documento_serializer_validation(self):
        """Test validación del DocumentoSerializer."""
        # Test sin título
        data = {'tipo': 'REPORT'}
        serializer = DocumentoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo', serializer.errors)
        
        # Test tipo inválido
        data = {
            'titulo': 'Test',
            'tipo': 'INVALID_TYPE',
            'archivo': self.test_file
        }
        serializer = DocumentoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
    @patch('documents.serializers.DocumentoSerializer.context')
    def test_documento_serializer_url_archivo_with_request(self, mock_context):
        """Test generación de URL absoluta con request en contexto."""
        mock_request = MagicMock()
        mock_request.build_absolute_uri.return_value = 'http://testserver/media/test.pdf'
        mock_context.get.return_value = mock_request
        
        serializer = DocumentoSerializer(self.documento)
        data = serializer.data
        
        # Should include absolute URL
        self.assertIsNotNone(data['url_archivo'])


class HistorialDocumentoSerializerTest(TestCase):
    """Test suite para HistorialDocumentoSerializer."""
    
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
        
        self.historial = HistorialDocumento.objects.create(
            documento=self.documento,
            usuario=self.user,
            tipo_cambio='CREATE',
            descripcion='Creación inicial',
            version_anterior=''
        )
        
    def test_historial_documento_serializer_read(self):
        """Test operaciones de lectura del HistorialDocumentoSerializer."""
        serializer = HistorialDocumentoSerializer(self.historial)
        data = serializer.data
        
        self.assertEqual(data['documento'], self.documento.id)
        self.assertEqual(data['usuario'], self.user.id)
        self.assertEqual(data['tipo_cambio'], 'CREATE')
        self.assertEqual(data['descripcion'], 'Creación inicial')
        self.assertIn('fecha', data)
        
    def test_historial_documento_serializer_create(self):
        """Test creación mediante HistorialDocumentoSerializer."""
        data = {
            'documento': self.documento.id,
            'tipo_cambio': 'UPDATE',
            'descripcion': 'Actualización de documento',
            'version_anterior': '1.0'
        }
        
        serializer = HistorialDocumentoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        historial = serializer.save(usuario=self.user)
        self.assertEqual(historial.tipo_cambio, 'UPDATE')
        self.assertEqual(historial.usuario, self.user)
        
    def test_historial_documento_serializer_readonly_fields(self):
        """Test campos de solo lectura del HistorialDocumentoSerializer."""
        readonly_data = {
            'fecha': '2024-01-01T00:00:00Z',
            'usuario': None
        }
        
        serializer = HistorialDocumentoSerializer(self.historial, data=readonly_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        # Los campos readonly no deberían cambiar
        historial_actualizado = serializer.save()
        self.assertEqual(historial_actualizado.usuario, self.user)


class DocumentsAPITestCase(APITestCase):
    """Test suite para los endpoints de la API de Documents."""
    
    def setUp(self):
        """Configurar datos de prueba y autenticación."""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
        )
        
        self.test_file = SimpleUploadedFile(
            'test_document.pdf',
            b'fake pdf content',
            content_type='application/pdf'
        )
        
        self.documento = Documento.objects.create(
            titulo='Documento de Prueba',
            tipo='REPORT',
            descripcion='Documento para testing',
            archivo=self.test_file,
            creado_por=self.admin_user,
            version='1.0'
        )
        
        self.client = APIClient()
        
    def authenticate_admin(self):
        """Autenticar como usuario admin."""
        self.client.force_authenticate(user=self.admin_user)
        
    def authenticate_regular(self):
        """Autenticar como usuario regular."""
        self.client.force_authenticate(user=self.regular_user)
        
    def test_documento_list_requires_authentication(self):
        """Test que listar documentos requiere autenticación."""
        url = reverse('documentos:documentos-list')
        
        # Solicitud sin autenticar
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Solicitud autenticada
        self.authenticate_admin()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_documento_create(self):
        """Test creación de documento via API."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-create')
        
        new_file = SimpleUploadedFile(
            'new_document.pdf',
            b'new pdf content',
            content_type='application/pdf'
        )
        
        data = {
            'titulo': 'Nuevo Documento API',
            'tipo': 'MANUAL',
            'descripcion': 'Documento creado via API',
            'archivo': new_file,
            'version': '1.0',
            'tags': 'api, test'
        }
        
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el documento se creó
        documento = Documento.objects.get(titulo='Nuevo Documento API')
        self.assertEqual(documento.creado_por, self.admin_user)
        
        # Verificar que se creó entrada en historial
        historial = HistorialDocumento.objects.filter(
            documento=documento,
            tipo_cambio='CREATE'
        ).first()
        self.assertIsNotNone(historial)
        
    def test_documento_detail_view(self):
        """Test vista de detalle de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-detail', kwargs={'pk': self.documento.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['titulo'], 'Documento de Prueba')
        self.assertEqual(data['tipo'], 'REPORT')
        
    def test_documento_update(self):
        """Test actualización de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-update', kwargs={'pk': self.documento.pk})
        
        update_data = {
            'titulo': 'Documento Actualizado via API',
            'descripcion': 'Descripción actualizada'
        }
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar actualización
        self.documento.refresh_from_db()
        self.assertEqual(self.documento.titulo, 'Documento Actualizado via API')
        
        # Verificar entrada en historial
        historial = HistorialDocumento.objects.filter(
            documento=self.documento,
            tipo_cambio='UPDATE'
        ).first()
        self.assertIsNotNone(historial)
        
    def test_documento_delete(self):
        """Test eliminación de documento."""
        self.authenticate_admin()
        url = reverse('documentos:documentos-delete', kwargs={'pk': self.documento.pk})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el documento se eliminó
        with self.assertRaises(Documento.DoesNotExist):
            Documento.objects.get(pk=self.documento.pk)


class DocumentsBusinessLogicTest(TestCase):
    """Test suite para lógica de negocio de documents."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_documento_file_size_formats(self):
        """Test diferentes formatos de tamaño de archivo."""
        # Test archivo en bytes
        small_file = SimpleUploadedFile('small.txt', b'x', content_type='text/plain')
        documento_small = Documento.objects.create(
            titulo='Archivo Pequeño',
            tipo='OTHER',
            archivo=small_file
        )
        self.assertIn('B', documento_small.tamano_archivo)
        
        # Test archivo en KB (simulado)
        medium_file = SimpleUploadedFile('medium.txt', b'x' * 2048, content_type='text/plain')
        documento_medium = Documento.objects.create(
            titulo='Archivo Mediano',
            tipo='OTHER',
            archivo=medium_file
        )
        self.assertIn('KB', documento_medium.tamano_archivo)
        
    def test_documento_version_management(self):
        """Test gestión de versiones de documentos."""
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Documento Versionado',
            tipo='REPORT',
            archivo=test_file,
            version='1.0'
        )
        
        # Crear historial de versión
        HistorialDocumento.objects.create(
            documento=documento,
            usuario=self.user,
            tipo_cambio='VERSION',
            descripcion='Nueva versión',
            version_anterior='1.0'
        )
        
        # Actualizar versión
        documento.version = '2.0'
        documento.save()
        
        self.assertEqual(documento.version, '2.0')
        
    def test_documento_tags_functionality(self):
        """Test funcionalidad de etiquetas."""
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        
        documento = Documento.objects.create(
            titulo='Documento con Tags',
            tipo='REPORT',
            archivo=test_file,
            tags='importante, urgente, reporte'
        )
        
        self.assertEqual(documento.tags, 'importante, urgente, reporte')
        
        # Test búsqueda por tags (esto sería implementado en views/filters)
        documentos_importantes = Documento.objects.filter(tags__icontains='importante')
        self.assertIn(documento, documentos_importantes)


class DocumentsSignalsTest(TestCase):
    """Test suite para señales de documents."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    @patch('documents.signals.delete_s3_files_from_instance')
    def test_delete_document_s3_files_signal(self, mock_delete_s3):
        """Test señal de eliminación de archivos S3."""
        mock_delete_s3.return_value = {'success': True}
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        documento = Documento.objects.create(
            titulo='Documento para Eliminar',
            tipo='REPORT',
            archivo=test_file,
            creado_por=self.user
        )
        
        # Eliminar documento
        documento.delete()
        
        # Verificar que se llamó la función de eliminación S3
        mock_delete_s3.assert_called_once()
        
    @patch('documents.signals.delete_old_s3_file')
    def test_delete_old_file_on_update_signal(self, mock_delete_old):
        """Test señal de eliminación de archivo anterior en actualización."""
        mock_delete_old.return_value = True
        
        test_file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        documento = Documento.objects.create(
            titulo='Documento para Actualizar',
            tipo='REPORT',
            archivo=test_file,
            creado_por=self.user
        )
        
        # Actualizar archivo
        new_file = SimpleUploadedFile('new.pdf', b'new content', content_type='application/pdf')
        documento.archivo = new_file
        documento.save()
        
        # Verificar que se llamó la función de eliminación del archivo anterior
        mock_delete_old.assert_called()