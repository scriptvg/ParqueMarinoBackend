# tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.business.payments.models import Pago, PagoInscripcion, Donacion
from apps.business.education.models import Inscripcion, Programa

User = get_user_model()

class TestPagoViewSet(TestCase):
    """Pruebas para el ViewSet de Pago
    
    Verifica las operaciones CRUD y permisos para pagos generales.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        
        self.pago_data = {
            'monto': '100.00',
            'moneda': 'USD',
            'metodo_pago': 'TARJETA',
            'referencia_transaccion': 'TEST-VIEW-001',
            'estado': 'PENDIENTE'
        }
        
        self.pago = Pago.objects.create(**self.pago_data)

    def test_listar_pagos_admin(self):
        """Prueba que un admin pueda ver todos los pagos"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('pago-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_pago_sin_autenticacion(self):
        """Prueba que no se puedan crear pagos sin autenticación"""
        response = self.client.post(reverse('pago-list'), self.pago_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modificar_pago_admin(self):
        """Prueba que un admin pueda modificar pagos"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'estado': 'COMPLETADO'}
        response = self.client.patch(
            reverse('pago-detail', kwargs={'pk': self.pago.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], 'COMPLETADO')

class TestPagoInscripcionViewSet(TestCase):
    """Pruebas para el ViewSet de PagoInscripcion
    
    Verifica las operaciones y validaciones específicas para pagos
    de inscripciones educativas.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.estudiante = User.objects.create_user(
            username='estudiante',
            email='estudiante@example.com',
            password='estudiante123'
        )
        
        self.programa = Programa.objects.create(
            nombre='Programa Test',
            precio=Decimal('500.00')
        )
        
        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            programa=self.programa,
            estado='PENDIENTE'
        )
        
        self.pago_inscripcion_data = {
            'inscripcion': self.inscripcion.id,
            'monto': '500.00',
            'moneda': 'USD',
            'metodo_pago': 'TARJETA',
            'referencia_transaccion': 'TEST-INSC-VIEW-001',
            'estado': 'PENDIENTE'
        }

    def test_procesar_pago_inscripcion(self):
        """Prueba el procesamiento de un pago de inscripción"""
        self.client.force_authenticate(user=self.estudiante)
        response = self.client.post(
            reverse('pagoinscripcion-procesar-pago', kwargs={'pk': self.inscripcion.pk}),
            self.pago_inscripcion_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado, 'COMPLETADO')

    def test_listar_pagos_inscripcion_estudiante(self):
        """Prueba que un estudiante solo vea sus pagos"""
        PagoInscripcion.objects.create(**self.pago_inscripcion_data)
        self.client.force_authenticate(user=self.estudiante)
        response = self.client.get(reverse('pagoinscripcion-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class TestDonacionViewSet(TestCase):
    """Pruebas para el ViewSet de Donacion
    
    Verifica las operaciones y validaciones específicas para donaciones.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.donacion_data = {
            'monto': '50.00',
            'moneda': 'USD',
            'nombre_donante': 'Juan Pérez',
            'email_donante': 'juan@example.com',
            'metodo_pago': 'TRANSFERENCIA',
            'referencia_transaccion': 'TEST-DON-VIEW-001',
            'estado': 'PENDIENTE'
        }

    def test_crear_donacion(self):
        """Prueba la creación de una donación"""
        response = self.client.post(reverse('donacion-list'), self.donacion_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donacion.objects.count(), 1)

    def test_procesar_donacion(self):
        """Prueba el procesamiento de una donación"""
        donacion = Donacion.objects.create(**self.donacion_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            reverse('donacion-procesar-donacion', kwargs={'pk': donacion.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        donacion.refresh_from_db()
        self.assertEqual(donacion.estado, 'COMPLETADO')

class TestMetodosPagoView(TestCase):
    """Pruebas para la vista de métodos de pago disponibles"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = APIClient()

    def test_obtener_metodos_pago(self):
        """Prueba obtener la lista de métodos de pago disponibles"""
        response = self.client.get(reverse('metodos-pago'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('TARJETA', response.data)
        self.assertIn('TRANSFERENCIA', response.data)
