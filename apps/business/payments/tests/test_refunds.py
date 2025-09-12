# tests/test_refunds.py

from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from apps.business.payments.models import Pago, Reembolso
from apps.business.payments.services import ReembolsoService
from apps.business.payments.exceptions import ReembolsoError

class TestReembolsoService(TestCase):
    """Pruebas para el servicio de reembolsos
    
    Verifica la creación, procesamiento y seguimiento de reembolsos
    para diferentes tipos de pagos y métodos de pago.
    """

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.service = ReembolsoService()
        
        # Crear pago de prueba
        self.pago = Pago.objects.create(
            monto=Decimal('100.00'),
            moneda='USD',
            estado='completado',
            metodo_pago='tarjeta',
            fecha_creacion=timezone.now(),
            referencia='PAY001'
        )

    def test_crear_reembolso_total(self):
        """Prueba la creación de un reembolso total"""
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Solicitud del cliente',
            monto=None  # Monto None indica reembolso total
        )
        
        self.assertEqual(reembolso.monto, self.pago.monto)
        self.assertEqual(reembolso.estado, 'pendiente')
        self.assertEqual(reembolso.tipo, 'total')

    def test_crear_reembolso_parcial(self):
        """Prueba la creación de un reembolso parcial"""
        monto_parcial = Decimal('50.00')
        
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Compensación parcial',
            monto=monto_parcial
        )
        
        self.assertEqual(reembolso.monto, monto_parcial)
        self.assertEqual(reembolso.tipo, 'parcial')

    def test_validar_monto_reembolso(self):
        """Prueba la validación de montos de reembolso"""
        # Intentar reembolsar más que el monto original
        with self.assertRaises(ReembolsoError):
            self.service.crear_reembolso(
                pago=self.pago,
                motivo='Prueba',
                monto=Decimal('150.00')
            )

    def test_multiple_reembolsos_parciales(self):
        """Prueba múltiples reembolsos parciales para un pago"""
        # Primer reembolso parcial
        reembolso1 = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Primera parte',
            monto=Decimal('30.00')
        )
        
        # Segundo reembolso parcial
        reembolso2 = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Segunda parte',
            monto=Decimal('40.00')
        )
        
        # Verificar monto disponible para reembolso
        monto_disponible = self.service.calcular_monto_disponible(self.pago)
        self.assertEqual(monto_disponible, Decimal('30.00'))

    @patch('payments.integrations.stripe_client.StripeClient.create_refund')
    def test_procesar_reembolso_tarjeta(self, mock_stripe_refund):
        """Prueba el procesamiento de reembolso para pago con tarjeta"""
        # Simular respuesta exitosa de Stripe
        mock_stripe_refund.return_value = {
            'success': True,
            'refund_id': 're_test123'
        }
        
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Reembolso a tarjeta'
        )
        
        resultado = self.service.procesar_reembolso(reembolso)
        
        self.assertTrue(resultado['success'])
        self.assertEqual(reembolso.estado, 'completado')
        self.assertEqual(reembolso.referencia_externa, 're_test123')

    @patch('payments.integrations.paypal.PayPalClient.refund_payment')
    def test_procesar_reembolso_paypal(self, mock_paypal_refund):
        """Prueba el procesamiento de reembolso para pago con PayPal"""
        # Cambiar método de pago a PayPal
        self.pago.metodo_pago = 'paypal'
        self.pago.save()
        
        # Simular respuesta exitosa de PayPal
        mock_paypal_refund.return_value = {
            'success': True,
            'refund_id': 'REF123'
        }
        
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Reembolso a PayPal'
        )
        
        resultado = self.service.procesar_reembolso(reembolso)
        
        self.assertTrue(resultado['success'])
        self.assertEqual(reembolso.estado, 'completado')

    def test_reembolso_pago_no_completado(self):
        """Prueba intentar reembolsar un pago no completado"""
        self.pago.estado = 'pendiente'
        self.pago.save()
        
        with self.assertRaises(ReembolsoError):
            self.service.crear_reembolso(
                pago=self.pago,
                motivo='Intento inválido'
            )

    def test_reembolso_ya_reembolsado(self):
        """Prueba intentar reembolsar un pago ya reembolsado"""
        # Crear reembolso total
        self.service.crear_reembolso(
            pago=self.pago,
            motivo='Primer reembolso'
        )
        
        # Intentar otro reembolso
        with self.assertRaises(ReembolsoError):
            self.service.crear_reembolso(
                pago=self.pago,
                motivo='Segundo intento'
            )

    def test_historial_reembolsos(self):
        """Prueba la obtención del historial de reembolsos"""
        # Crear varios reembolsos
        reembolso1 = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Primer reembolso parcial',
            monto=Decimal('30.00')
        )
        
        reembolso2 = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Segundo reembolso parcial',
            monto=Decimal('20.00')
        )
        
        historial = self.service.obtener_historial_reembolsos(self.pago)
        
        self.assertEqual(len(historial), 2)
        self.assertEqual(
            sum(r.monto for r in historial),
            Decimal('50.00')
        )

    def test_notificacion_reembolso(self):
        """Prueba la generación de notificaciones de reembolso"""
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Reembolso con notificación'
        )
        
        with patch('payments.notifications.PaymentNotifier.send_refund_confirmation') as mock_notify:
            self.service.procesar_reembolso(reembolso)
            mock_notify.assert_called_once()

    def test_reembolso_diferentes_monedas(self):
        """Prueba reembolsos con diferentes monedas"""
        # Cambiar moneda del pago
        self.pago.moneda = 'EUR'
        self.pago.save()
        
        reembolso = self.service.crear_reembolso(
            pago=self.pago,
            motivo='Reembolso en EUR'
        )