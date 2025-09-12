# tests/test_notifications.py

from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core import mail
from django.template.loader import render_to_string
from decimal import Decimal
from apps.business.payments.notifications import PaymentNotifier, EmailError
from apps.business.payments.models import Pago, PagoInscripcion, Donacion
from django.contrib.auth import get_user_model

User = get_user_model()

class TestPaymentNotifier(TestCase):
    """Pruebas para el servicio de notificaciones por email
    
    Verifica el envío de correos electrónicos para diferentes eventos
    relacionados con pagos, incluyendo confirmaciones, fallos y facturas.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.notifier = PaymentNotifier()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.pago = Pago.objects.create(
            monto=Decimal('100.00'),
            moneda='USD',
            metodo_pago='TARJETA',
            referencia_transaccion='TEST-NOT-001',
            estado='COMPLETADO'
        )

    def test_enviar_confirmacion_pago(self):
        """Prueba el envío de confirmación de pago"""
        self.notifier.enviar_confirmacion_pago(
            self.pago,
            'test@example.com',
            {'site_name': 'Test Site'}
        )
        
        # Verifica que se envió el email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'test@example.com')
        self.assertIn('Confirmación de Pago', mail.outbox[0].subject)

    def test_enviar_notificacion_fallo(self):
        """Prueba el envío de notificación de fallo de pago"""
        error_data = {
            'mensaje': 'Fondos insuficientes',
            'codigo': 'INSUFFICIENT_FUNDS'
        }
        
        self.notifier.enviar_notificacion_fallo(
            self.pago,
            'test@example.com',
            error_data,
            {'site_name': 'Test Site'}
        )
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Pago No Procesado', mail.outbox[0].subject)
        self.assertIn('Fondos insuficientes', mail.outbox[0].body)

    @patch('payments.notifications.render_to_string')
    def test_renderizado_plantilla(self, mock_render):
        """Prueba el renderizado de plantillas de email"""
        mock_render.return_value = 'Contenido del email'
        
        self.notifier.enviar_confirmacion_pago(
            self.pago,
            'test@example.com',
            {'site_name': 'Test Site'}
        )
        
        mock_render.assert_called_with(
            'payments/email/payment_confirmation.html',
            {'payment': self.pago, 'site_name': 'Test Site'}
        )

    def test_manejo_error_email(self):
        """Prueba el manejo de errores al enviar emails"""
        with patch('django.core.mail.send_mail') as mock_send:
            mock_send.side_effect = Exception('Error de envío')
            
            with self.assertRaises(EmailError):
                self.notifier.enviar_confirmacion_pago(
                    self.pago,
                    'test@example.com',
                    {'site_name': 'Test Site'}
                )

    def test_enviar_factura_electronica(self):
        """Prueba el envío de factura electrónica por email"""
        factura_data = {
            'numero': 'FE-001',
            'xml_content': '<xml>...</xml>',
            'pdf_content': b'PDF content'
        }
        
        self.notifier.enviar_factura_electronica(
            self.pago,
            'test@example.com',
            factura_data,
            {'company_name': 'Test Company'}
        )
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 2)  # XML y PDF
        self.assertIn('Factura Electrónica', mail.outbox[0].subject)

    def test_enviar_confirmacion_donacion(self):
        """Prueba el envío de confirmación de donación"""
        donacion = Donacion.objects.create(
            monto=Decimal('50.00'),
            moneda='USD',
            nombre_donante='Juan Pérez',
            email_donante='juan@example.com',
            metodo_pago='TRANSFERENCIA',
            referencia_transaccion='TEST-DON-001',
            estado='COMPLETADO'
        )
        
        self.notifier.enviar_confirmacion_donacion(
            donacion,
            {'organization_name': 'ONG Test'}
        )
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'juan@example.com')
        self.assertIn('¡Gracias por su Donación!', mail.outbox[0].subject)

    def test_enviar_confirmacion_reembolso(self):
        """Prueba el envío de confirmación de reembolso"""
        reembolso_data = {
            'monto': Decimal('100.00'),
            'fecha': '2024-01-20',
            'metodo': 'TARJETA'
        }
        
        self.notifier.enviar_confirmacion_reembolso(
            self.pago,
            'test@example.com',
            reembolso_data,
            {'support_phone': '88888888'}
        )
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Reembolso Confirmado', mail.outbox[0].subject)

    def test_validacion_email(self):
        """Prueba la validación de direcciones de email"""
        with self.assertRaises(EmailError):
            self.notifier.enviar_confirmacion_pago(
                self.pago,
                'email_invalido',
                {'site_name': 'Test Site'}
            )

    def test_multiples_destinatarios(self):
        """Prueba el envío a múltiples destinatarios"""
        destinatarios = ['test1@example.com', 'test2@example.com']
        
        self.notifier.enviar_confirmacion_pago(
            self.pago,
            destinatarios,
            {'site_name': 'Test Site'}
        )
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 2)