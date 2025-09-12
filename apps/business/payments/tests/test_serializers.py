# tests/test_serializers.py

from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.business.payments.models import Pago, PagoInscripcion, Donacion
from apps.business.payments.serializers import PagoSerializer, PagoInscripcionSerializer, DonacionSerializer
from apps.business.education.models import Inscripcion, Programa

User = get_user_model()

class TestPagoSerializer(TestCase):
    """Pruebas para el serializador de Pago
    
    Verifica la correcta serialización y deserialización de pagos,
    incluyendo validaciones y formateo de datos monetarios.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.pago_data = {
            'monto': '100.00',
            'moneda': 'USD',
            'metodo_pago': 'TARJETA',
            'referencia_transaccion': 'TEST-SER-001',
            'estado': 'PENDIENTE',
            'notas': 'Pago de prueba'
        }
        
        self.pago = Pago.objects.create(**self.pago_data)
        self.serializer = PagoSerializer(instance=self.pago)

    def test_contiene_campos_esperados(self):
        """Verifica que el serializer incluya todos los campos necesarios"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'fecha_pago', 'monto', 'moneda', 'monto_crc', 'monto_usd',
            'metodo_pago', 'referencia_transaccion', 'estado', 'comprobante',
            'notas'
        ]))

    def test_validacion_monto_positivo(self):
        """Prueba que el serializer valide montos positivos"""
        data = self.pago_data.copy()
        data['monto'] = '-100.00'
        serializer = PagoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('monto', serializer.errors)

    def test_validacion_referencia_unica(self):
        """Prueba que no se permitan referencias duplicadas"""
        data = self.pago_data.copy()
        serializer = PagoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('referencia_transaccion', serializer.errors)

class TestPagoInscripcionSerializer(TestCase):
    """Pruebas para el serializador de PagoInscripcion
    
    Verifica la correcta serialización y validación de pagos asociados
    a inscripciones en programas educativos.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.programa = Programa.objects.create(
            nombre='Programa Test',
            precio=Decimal('500.00')
        )
        
        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.user,
            programa=self.programa,
            estado='PENDIENTE'
        )
        
        self.pago_inscripcion_data = {
            'inscripcion': self.inscripcion.id,
            'monto': '500.00',
            'moneda': 'USD',
            'metodo_pago': 'TARJETA',
            'referencia_transaccion': 'TEST-INSC-SER-001',
            'estado': 'PENDIENTE'
        }

    def test_validacion_monto_programa(self):
        """Prueba que el monto coincida con el precio del programa"""
        data = self.pago_inscripcion_data.copy()
        data['monto'] = '400.00'  # Monto incorrecto
        serializer = PagoInscripcionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('monto', serializer.errors)

    def test_validacion_inscripcion_unica(self):
        """Prueba que no se permitan múltiples pagos para una inscripción"""
        PagoInscripcion.objects.create(**self.pago_inscripcion_data)
        serializer = PagoInscripcionSerializer(data=self.pago_inscripcion_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('inscripcion', serializer.errors)

class TestDonacionSerializer(TestCase):
    """Pruebas para el serializador de Donacion
    
    Verifica la correcta serialización y validación de donaciones,
    incluyendo datos del donante y montos.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.donacion_data = {
            'monto': '50.00',
            'moneda': 'USD',
            'nombre_donante': 'Juan Pérez',
            'email_donante': 'juan@example.com',
            'metodo_pago': 'TRANSFERENCIA',
            'referencia_transaccion': 'TEST-DON-SER-001',
            'estado': 'COMPLETADO'
        }
        
        self.donacion = Donacion.objects.create(**self.donacion_data)
        self.serializer = DonacionSerializer(instance=self.donacion)

    def test_contiene_campos_esperados(self):
        """Verifica que el serializer incluya todos los campos necesarios"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'monto', 'moneda', 'monto_crc', 'monto_usd',
            'nombre_donante', 'email_donante', 'metodo_pago',
            'referencia_transaccion', 'estado'
        ]))

    def test_validacion_datos_donante(self):
        """Prueba que se requieran ambos campos de donante si uno está presente"""
        data = self.donacion_data.copy()
        data['email_donante'] = ''
        serializer = DonacionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email_donante', serializer.errors)

    def test_validacion_email_formato(self):
        """Prueba que el email tenga un formato válido"""
        data = self.donacion_data.copy()
        data['email_donante'] = 'email_invalido'
        serializer = DonacionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email_donante', serializer.errors)