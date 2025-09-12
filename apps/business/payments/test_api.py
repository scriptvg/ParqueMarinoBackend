from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Pago, PagoInscripcion, Donacion
from .serializers import PagoSerializer, PagoInscripcionSerializer, DonacionSerializer
from apps.business.education.models import Instructor, Programa, Horario, Inscripcion

User = get_user_model()


class PagoSerializerTest(TestCase):
    """Test suite para PagoSerializer."""
    
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_serializer_creation(self, mock_currency):
        """Test creación de pago usando serializer."""
        mock_currency.return_value = (Decimal('54000.00'), Decimal('100.00'))
        
        data = {
            'monto': '100.00',
            'moneda': 'USD',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'SER123456',
            'estado': 'PENDING'
        }
        
        serializer = PagoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        pago = serializer.save()
        self.assertEqual(pago.monto, Decimal('100.00'))
        self.assertEqual(pago.moneda, 'USD')
        self.assertEqual(pago.monto_crc, Decimal('54000.00'))
        self.assertEqual(pago.monto_usd, Decimal('100.00'))
        
    def test_pago_serializer_validation_monto_negativo(self):
        """Test validación de monto negativo en serializer."""
        data = {
            'monto': '-50.00',
            'moneda': 'USD',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'NEG123'
        }
        
        serializer = PagoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('monto', serializer.errors)
        self.assertTrue(
            'mayor a cero' in str(serializer.errors['monto']) or 
            'mayor o igual a 0' in str(serializer.errors['monto'])
        )
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_serializer_validation_referencia_duplicada(self, mock_currency):
        """Test validación de referencia de transacción duplicada."""
        mock_currency.return_value = (Decimal('25000.00'), Decimal('46.30'))
        
        # Crear primer pago
        Pago.objects.create(
            monto=Decimal('46.30'),
            moneda='USD',
            metodo_pago='CARD',
            referencia_transaccion='DUP123'
        )
        
        # Intentar crear segundo pago con misma referencia
        data = {
            'monto': '75.00',
            'moneda': 'USD',
            'metodo_pago': 'PAYPAL',
            'referencia_transaccion': 'DUP123'
        }
        
        serializer = PagoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('referencia_transaccion', serializer.errors)
        self.assertTrue(
            'ya existe' in str(serializer.errors['referencia_transaccion']) or 
            'Ya existe' in str(serializer.errors['referencia_transaccion'])
        ) or self.assertIn('Ya existe', str(serializer.errors['referencia_transaccion']))


class PagoInscripcionSerializerTest(TestCase):
    """Test suite para PagoInscripcionSerializer."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user_instructor = User.objects.create_user(username='instructor_api')
        self.user_participant = User.objects.create_user(username='participant_api')
        
        self.instructor = Instructor.objects.create(
            user=self.user_instructor,
            especialidad='Biología Marina',
            experiencia_years=5,
            bio='Instructor para API tests'
        )
        
        self.programa = Programa.objects.create(
            nombre='Programa API Test',
            descripcion='Programa para pruebas de API',
            duracion_horas=2,
            capacidad_min=3,
            capacidad_max=15,
            edad_minima=8,
            edad_maxima=14,
            requisitos='Ninguno',
            precio=Decimal('25000.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=5)
        fecha_fin = fecha_inicio + timedelta(hours=2)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cupos_disponibles=15
        )
        
        self.inscripcion = Inscripcion.objects.create(
            usuario=self.user_participant,
            horario=self.horario,
            nombre_participante='Participante API Test',
            edad_participante=12,
            fecha_inscripcion=timezone.now()
        )
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_inscripcion_serializer_creation(self, mock_currency):
        """Test creación de pago de inscripción usando serializer."""
        mock_currency.return_value = (Decimal('25000.00'), Decimal('46.30'))
        
        data = {
            'inscripcion': self.inscripcion.id,
            'monto': '25000.00',
            'moneda': 'CRC',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'INS123456'
        }
        
        serializer = PagoInscripcionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f'Serializer errors: {serializer.errors}')
        
        pago_inscripcion = serializer.save()
        self.assertEqual(pago_inscripcion.inscripcion, self.inscripcion)
        self.assertEqual(pago_inscripcion.monto, Decimal('25000.00'))
        
    def test_pago_inscripcion_serializer_validation_pago_existente(self):
        """Test validación de pago existente para inscripción."""
        # Crear un pago existente para la inscripción
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('25000.00'), Decimal('46.30'))
            
            PagoInscripcion.objects.create(
                inscripcion=self.inscripcion,
                monto=self.programa.precio,
                moneda='CRC',
                metodo_pago='CARD',
                referencia_transaccion='EXISTING123'
            )
            
            # Intentar crear otro pago para la misma inscripción
            data = {
                'inscripcion': self.inscripcion.id,
                'monto': '25000.00',
                'moneda': 'CRC',
                'metodo_pago': 'PAYPAL',
                'referencia_transaccion': 'DUPLICATE123'
            }
            
            serializer = PagoInscripcionSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            # Check if error is in non_field_errors or in inscripcion field
            self.assertTrue(
                'non_field_errors' in serializer.errors or
                'inscripcion' in serializer.errors
            )
        
    def test_pago_inscripcion_serializer_validation_monto_incorrecto(self):
        """Test validación de monto incorrecto para el programa."""
        data = {
            'inscripcion': self.inscripcion.id,
            'monto': '30000.00',  # Monto diferente al precio del programa
            'moneda': 'CRC',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'WRONG123'
        }
        
        serializer = PagoInscripcionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Check if error is in non_field_errors or in a specific field
        self.assertTrue(
            'non_field_errors' in serializer.errors or 
            any('no coincide' in str(error) for error_list in serializer.errors.values() for error in error_list)
        )


class DonacionSerializerTest(TestCase):
    """Test suite para DonacionSerializer."""
    
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_donacion_serializer_creation(self, mock_currency):
        """Test creación de donación usando serializer."""
        mock_currency.return_value = (Decimal('54000.00'), Decimal('100.00'))
        
        data = {
            'monto': '100.00',
            'moneda': 'USD',
            'nombre_donante': 'María González',
            'email_donante': 'maria@example.com',
            'metodo_pago': 'PAYPAL',
            'referencia_transaccion': 'DON123456'
        }
        
        serializer = DonacionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        donacion = serializer.save()
        self.assertEqual(donacion.monto, Decimal('100.00'))
        self.assertEqual(donacion.nombre_donante, 'María González')
        self.assertEqual(donacion.email_donante, 'maria@example.com')
        
    def test_donacion_serializer_validation_monto_negativo(self):
        """Test validación de monto negativo en donación."""
        data = {
            'monto': '-25.00',
            'moneda': 'USD',
            'nombre_donante': 'Juan Pérez',
            'email_donante': 'juan@example.com',
            'metodo_pago': 'CARD'
        }
        
        serializer = DonacionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('monto', serializer.errors)
        self.assertTrue(
            'mayor a cero' in str(serializer.errors['monto']) or 
            'mayor o igual a 0' in str(serializer.errors['monto'])
        )


class PagoAPITest(APITestCase):
    """Test suite para API de pagos."""
    
    def setUp(self):
        """Configurar datos de prueba para API tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = APIClient()
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_create_pago_authenticated(self, mock_currency):
        """Test creación de pago con usuario autenticado."""
        mock_currency.return_value = (Decimal('50000.00'), Decimal('92.59'))
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            'monto': '92.59',
            'moneda': 'USD',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'API123456',
            'estado': 'PENDING'
        }
        
        url = '/api/payments/pagos/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pago.objects.count(), 1)
        
        pago = Pago.objects.first()
        self.assertEqual(pago.monto, Decimal('92.59'))
        self.assertEqual(pago.referencia_transaccion, 'API123456')
        
    def test_create_pago_unauthenticated(self):
        """Test creación de pago sin autenticación."""
        data = {
            'monto': '50.00',
            'moneda': 'USD',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'UNAUTH123'
        }
        
        url = '/api/payments/pagos/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_update_pago_as_admin_only(self, mock_currency):
        """Test actualización de pago solo como administrador."""
        mock_currency.return_value = (Decimal('35000.00'), Decimal('64.81'))
        
        pago = Pago.objects.create(
            monto=Decimal('64.81'),
            moneda='USD',
            metodo_pago='CARD',
            referencia_transaccion='UPDATE123',
            estado='PENDING'
        )
        
        # Intentar actualizar como usuario normal (sin permisos de admin)
        self.client.force_authenticate(user=self.user)
        url = f'/api/payments/admin/pagos/{pago.id}/update/'
        data = {'estado': 'SUCCESS'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Actualizar como administrador
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pago.refresh_from_db()
        self.assertEqual(pago.estado, 'SUCCESS')


class PagoInscripcionAPITest(APITestCase):
    """Test suite para API de pagos de inscripción."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='participant_api',
            email='participant@example.com',
            password='pass123'
        )
        
        # Crear instructor y programa
        instructor_user = User.objects.create_user(username='instructor_api_test')
        self.instructor = Instructor.objects.create(
            user=instructor_user,
            especialidad='Biología',
            experiencia_years=3,
            bio='Instructor API test'
        )
        
        self.programa = Programa.objects.create(
            nombre='Programa API Test',
            descripcion='Programa para API testing',
            duracion_horas=3,
            capacidad_min=5,
            capacidad_max=20,
            edad_minima=10,
            edad_maxima=16,
            requisitos='Ninguno',
            precio=Decimal('45000.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=10)
        fecha_fin = fecha_inicio + timedelta(hours=3)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cupos_disponibles=20
        )
        
        self.inscripcion = Inscripcion.objects.create(
            usuario=self.user,
            horario=self.horario,
            nombre_participante='Participante API Test 2',
            edad_participante=14,
            fecha_inscripcion=timezone.now()
        )
        
        self.client = APIClient()
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_create_pago_inscripcion(self, mock_currency):
        """Test creación de pago de inscripción via API."""
        mock_currency.return_value = (Decimal('45000.00'), Decimal('83.33'))
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            'inscripcion': self.inscripcion.id,
            'monto': '45000.00',
            'moneda': 'CRC',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'INSCAPI123'
        }
        
        url = '/api/payments/pagos-inscripcion/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PagoInscripcion.objects.count(), 1)
        
        pago_inscripcion = PagoInscripcion.objects.first()
        self.assertEqual(pago_inscripcion.inscripcion, self.inscripcion)
        self.assertEqual(pago_inscripcion.monto, Decimal('45000.00'))
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_procesar_pago_inscripcion(self, mock_currency):
        """Test procesamiento de pago de inscripción."""
        mock_currency.return_value = (Decimal('45000.00'), Decimal('83.33'))
        
        # Crear pago de inscripción
        pago_inscripcion = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            monto=self.programa.precio,
            moneda='CRC',
            metodo_pago='CARD',
            referencia_transaccion='PROCESAR123',
            estado='PENDING'
        )
        
        # Authenticate as regular user (the procesar_pago endpoint is in the regular viewset)
        self.client.force_authenticate(user=self.user)
        # Use the correct URL pattern from pagos_inscripcion_urls.py
        url = f'/api/payments/pagos-inscripcion/{pago_inscripcion.id}/procesar_pago/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        pago_inscripcion.refresh_from_db()
        self.assertEqual(pago_inscripcion.estado, 'SUCCESS')


class DonacionAPITest(APITestCase):
    """Test suite para API de donaciones."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.client = APIClient()
        # Crear usuario admin para tests que requieren autenticación
        self.admin_user = User.objects.create_superuser(
            username='admin_donations',
            email='admin@donations.com',
            password='adminpass123'
        )
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_create_donacion_publica(self, mock_currency):
        """Test creación de donación sin autenticación."""
        mock_currency.return_value = (Decimal('50000.00'), Decimal('92.59'))
        
        data = {
            'monto': '92.59',
            'moneda': 'USD',
            'nombre_donante': 'Carlos Mendoza',
            'email_donante': 'carlos@example.com',
            'metodo_pago': 'PAYPAL',
            'referencia_transaccion': 'DONPUB123'
        }
        
        url = '/api/payments/donaciones/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donacion.objects.count(), 1)
        
        donacion = Donacion.objects.first()
        self.assertEqual(donacion.nombre_donante, 'Carlos Mendoza')
        self.assertEqual(donacion.email_donante, 'carlos@example.com')
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_create_donacion_anonima(self, mock_currency):
        """Test creación de donación anónima."""
        mock_currency.return_value = (Decimal('27000.00'), Decimal('50.00'))
        
        data = {
            'monto': '50.00',
            'moneda': 'USD',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'ANON123',
            'estado': 'PENDING'
        }
        
        url = '/api/payments/donaciones/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        donacion = Donacion.objects.first()
        self.assertIsNone(donacion.nombre_donante)
        self.assertIsNone(donacion.email_donante)


class PaymentIntegrationTest(APITestCase):
    """Test suite para integración completa del sistema de pagos."""
    
    def setUp(self):
        """Configurar escenario completo de prueba."""
        self.user = User.objects.create_user(
            username='integration_user',
            email='integration@example.com',
            password='integpass123'
        )
        
        # Crear instructor y programa
        instructor_user = User.objects.create_user(username='instructor_integration')
        self.instructor = Instructor.objects.create(
            user=instructor_user,
            especialidad='Conservación Marina',
            experiencia_years=8,
            bio='Instructor para tests de integración'
        )
        
        self.programa = Programa.objects.create(
            nombre='Programa Integración',
            descripcion='Programa para test de integración completa',
            duracion_horas=4,
            capacidad_min=3,
            capacidad_max=12,
            edad_minima=12,
            edad_maxima=18,
            requisitos='Saber nadar',
            precio=Decimal('65000.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=14)
        fecha_fin = fecha_inicio + timedelta(hours=4)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cupos_disponibles=12
        )
        
        self.client = APIClient()
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_flujo_completo_inscripcion_y_pago(self, mock_currency):
        """Test flujo completo: inscripción + pago + procesamiento."""
        mock_currency.return_value = (Decimal('65000.00'), Decimal('120.37'))
        
        self.client.force_authenticate(user=self.user)
        
        # 1. Crear inscripción
        inscripcion = Inscripcion.objects.create(
            usuario=self.user,
            horario=self.horario,
            nombre_participante='Participante Integración',
            edad_participante=16,
            fecha_inscripcion=timezone.now()
        )
        
        # 2. Crear pago de inscripción
        data_pago = {
            'inscripcion': inscripcion.id,
            'monto': '65000.00',
            'moneda': 'CRC',
            'metodo_pago': 'CARD',
            'referencia_transaccion': 'INTEGRATION123'
        }
        
        url_pago = '/api/payments/pagos-inscripcion/create/'
        response_pago = self.client.post(url_pago, data_pago)
        
        self.assertEqual(response_pago.status_code, status.HTTP_201_CREATED)
        
        # 3. Procesar pago
        pago_id = response_pago.data['id']
        url_procesar = f'/api/payments/pagos-inscripcion/{pago_id}/procesar_pago/'
        response_procesar = self.client.post(url_procesar)
        
        self.assertEqual(response_procesar.status_code, status.HTTP_200_OK)
        
        # 4. Verificar estado final
        pago_inscripcion = PagoInscripcion.objects.get(id=pago_id)
        self.assertEqual(pago_inscripcion.estado, 'SUCCESS')
        self.assertEqual(pago_inscripcion.inscripcion, inscripcion)
