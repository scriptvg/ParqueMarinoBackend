from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Pago, PagoInscripcion, Donacion
from .serializers import PagoSerializer, PagoInscripcionSerializer, DonacionSerializer
from apps.business.education.models import Instructor, Programa, Horario, Inscripcion
from .integrations.stripe_client import StripeClient

User = get_user_model()


class StripeIntegrationTest(TestCase):
    """Test suite para la integración con Stripe."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    @patch('payments.integrations.stripe_client.stripe.PaymentIntent.create')
    def test_stripe_client_create_payment_intent(self, mock_create):
        """Test creación de intención de pago con Stripe."""
        # Configurar el mock
        mock_create.return_value = MagicMock(
            id='pi_123',
            client_secret='secret_123',
            status='requires_payment_method'
        )
        
        # Crear cliente de Stripe
        stripe_client = StripeClient()
        
        # Crear intención de pago
        result = stripe_client.create_payment_intent(
            amount=Decimal('100.00'),
            currency='usd',
            description='Test payment'
        )
        
        # Verificar resultados
        self.assertEqual(result['id'], 'pi_123')
        self.assertEqual(result['client_secret'], 'secret_123')
        self.assertEqual(result['amount'], Decimal('100.00'))
        self.assertEqual(result['currency'], 'usd')
        self.assertEqual(result['status'], 'requires_payment_method')
        
        # Verificar que se llamó al método correcto
        mock_create.assert_called_once()


class PagoStripeAPITest(APITestCase):
    """Test suite para API de pagos con integración Stripe."""
    
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
        
    @patch('payments.integrations.stripe_client.stripe.PaymentIntent.create')
    def test_create_pago_with_stripe(self, mock_create):
        """Test creación de pago con procesamiento Stripe."""
        # Configurar el mock
        mock_create.return_value = MagicMock(
            id='pi_123',
            client_secret='secret_123',
            status='requires_payment_method'
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Crear un pago
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
        
        # Procesar el pago con Stripe
        url_procesar = f'/api/payments/pagos/{pago.id}/procesar_pago/'
        response_procesar = self.client.post(url_procesar)
        
        self.assertEqual(response_procesar.status_code, status.HTTP_200_OK)
        self.assertIn('payment_intent_id', response_procesar.data)
        self.assertIn('client_secret', response_procesar.data)
        self.assertIn('notification', response_procesar.data)
        
        # Verificar que el estado del pago se actualizó
        pago.refresh_from_db()
        self.assertEqual(pago.estado, 'SUCCESS')
        self.assertEqual(pago.referencia_transaccion, 'pi_123')


class PagoInscripcionStripeAPITest(APITestCase):
    """Test suite para API de pagos de inscripción con integración Stripe."""
    
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
        
    @patch('payments.integrations.stripe_client.stripe.PaymentIntent.create')
    def test_create_pago_inscripcion_with_stripe(self, mock_create):
        """Test creación de pago de inscripción con procesamiento Stripe."""
        # Configurar el mock
        mock_create.return_value = MagicMock(
            id='pi_inscripcion_123',
            client_secret='secret_inscripcion_123',
            status='requires_payment_method'
        )
        
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
        
        # Procesar el pago con Stripe
        url_procesar = f'/api/payments/pagos-inscripcion/{pago_inscripcion.id}/procesar_pago/'
        response_procesar = self.client.post(url_procesar)
        
        self.assertEqual(response_procesar.status_code, status.HTTP_200_OK)
        self.assertIn('payment_intent_id', response_procesar.data)
        self.assertIn('client_secret', response_procesar.data)
        self.assertIn('notification', response_procesar.data)
        
        # Verificar que el estado del pago se actualizó
        pago_inscripcion.refresh_from_db()
        self.assertEqual(pago_inscripcion.estado, 'SUCCESS')
        self.assertEqual(pago_inscripcion.referencia_transaccion, 'pi_inscripcion_123')


class DonacionStripeAPITest(APITestCase):
    """Test suite para API de donaciones con integración Stripe."""
    
    def setUp(self):
        """Configurar datos de prueba."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        
    @patch('payments.integrations.stripe_client.stripe.PaymentIntent.create')
    def test_create_donacion_with_stripe(self, mock_create):
        """Test creación de donación con procesamiento Stripe."""
        # Configurar el mock
        mock_create.return_value = MagicMock(
            id='pi_donacion_123',
            client_secret='secret_donacion_123',
            status='requires_payment_method'
        )
        
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        
        data = {
            'monto': '92.59',
            'moneda': 'USD',
            'nombre_donante': 'Carlos Mendoza',
            'email_donante': 'carlos@example.com',
            'metodo_pago': 'CARD'
        }
        
        url = '/api/payments/donaciones/create/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donacion.objects.count(), 1)
        
        donacion = Donacion.objects.first()
        self.assertEqual(donacion.nombre_donante, 'Carlos Mendoza')
        self.assertEqual(donacion.email_donante, 'carlos@example.com')
        
        # Procesar la donación con Stripe
        url_procesar = f'/api/payments/donaciones/{donacion.id}/procesar_pago/'
        response_procesar = self.client.post(url_procesar)
        
        self.assertEqual(response_procesar.status_code, status.HTTP_200_OK)
        self.assertIn('payment_intent_id', response_procesar.data)
        self.assertIn('client_secret', response_procesar.data)
        self.assertIn('notification', response_procesar.data)
        
        # Verificar que el estado de la donación se actualizó
        donacion.refresh_from_db()
        self.assertEqual(donacion.estado, 'SUCCESS')
        self.assertEqual(donacion.referencia_transaccion, 'pi_donacion_123')
