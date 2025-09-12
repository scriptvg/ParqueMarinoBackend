# tests/test_paypal.py

from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from decimal import Decimal
from apps.integrations.payments.paypal import PayPalClient, PayPalError

@override_settings(
    PAYPAL_CLIENT_ID='test_client_id',
    PAYPAL_CLIENT_SECRET='test_client_secret',
    PAYPAL_SANDBOX=True,
    PAYPAL_RETURN_URL='http://example.com/success',
    PAYPAL_CANCEL_URL='http://example.com/cancel'
)
class TestPayPalClient(TestCase):
    """Pruebas para la integración con PayPal
    
    Verifica la creación, ejecución y reembolso de pagos a través
    de la API de PayPal.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = PayPalClient()
        
        self.payment_data = {
            'amount': Decimal('100.00'),
            'currency': 'USD',
            'description': 'Curso de Programación'
        }

    @patch('paypalrestsdk.Payment')
    def test_create_payment_success(self, mock_payment):
        """Prueba la creación exitosa de un pago en PayPal"""
        # Simula respuesta exitosa de PayPal
        mock_payment_instance = MagicMock()
        mock_payment_instance.create.return_value = True
        mock_payment_instance.id = 'PAY-TEST123'
        mock_payment_instance.links = [
            MagicMock(rel='approval_url', href='https://paypal.com/approve'),
            MagicMock(rel='self', href='https://paypal.com/self')
        ]
        mock_payment.return_value = mock_payment_instance

        response = self.client.create_payment(**self.payment_data)
        
        self.assertEqual(response['id'], 'PAY-TEST123')
        self.assertEqual(response['approval_url'], 'https://paypal.com/approve')
        self.assertIn('links', response)

    @patch('paypalrestsdk.Payment')
    def test_create_payment_failure(self, mock_payment):
        """Prueba el manejo de errores al crear un pago"""
        # Simula error de PayPal
        mock_payment_instance = MagicMock()
        mock_payment_instance.create.return_value = False
        mock_payment_instance.error = {'message': 'Invalid request'}
        mock_payment.return_value = mock_payment_instance

        with self.assertRaises(PayPalError):
            self.client.create_payment(**self.payment_data)

    @patch('paypalrestsdk.Payment')
    def test_execute_payment_success(self, mock_payment):
        """Prueba la ejecución exitosa de un pago aprobado"""
        # Simula pago existente
        mock_payment_instance = MagicMock()
        mock_payment_instance.execute.return_value = True
        mock_payment_instance.id = 'PAY-TEST123'
        mock_payment_instance.state = 'approved'
        mock_payment_instance.transactions = [{'amount': {'total': '100.00', 'currency': 'USD'}}]
        mock_payment.find.return_value = mock_payment_instance

        result = self.client.execute_payment(
            payment_id='PAY-TEST123',
            payer_id='PAYER123'
        )
        
        self.assertEqual(result['id'], 'PAY-TEST123')
        self.assertEqual(result['state'], 'approved')

    @patch('paypalrestsdk.Payment')
    def test_execute_payment_failure(self, mock_payment):
        """Prueba el manejo de errores al ejecutar un pago"""
        # Simula error en la ejecución
        mock_payment_instance = MagicMock()
        mock_payment_instance.execute.return_value = False
        mock_payment_instance.error = {'message': 'Insufficient funds'}
        mock_payment.find.return_value = mock_payment_instance

        with self.assertRaises(PayPalError):
            self.client.execute_payment(
                payment_id='PAY-TEST123',
                payer_id='PAYER123'
            )

    @patch('paypalrestsdk.Sale')
    def test_refund_payment_success(self, mock_sale):
        """Prueba el reembolso exitoso de un pago"""
        # Simula reembolso exitoso
        mock_refund = MagicMock()
        mock_refund.success.return_value = True
        mock_refund.id = 'REFUND-TEST123'
        mock_refund.state = 'completed'
        mock_refund.amount = {'total': '100.00', 'currency': 'USD'}
        
        mock_sale_instance = MagicMock()
        mock_sale_instance.refund.return_value = mock_refund
        mock_sale.find.return_value = mock_sale_instance

        result = self.client.refund_payment(
            sale_id='SALE-TEST123',
            amount=Decimal('100.00')
        )
        
        self.assertEqual(result['id'], 'REFUND-TEST123')
        self.assertEqual(result['state'], 'completed')

    @patch('paypalrestsdk.Sale')
    def test_refund_payment_failure(self, mock_sale):
        """Prueba el manejo de errores al reembolsar un pago"""
        # Simula error en el reembolso
        mock_refund = MagicMock()
        mock_refund.success.return_value = False
        mock_refund.error = {'message': 'Refund failed'}
        
        mock_sale_instance = MagicMock()
        mock_sale_instance.refund.return_value = mock_refund
        mock_sale.find.return_value = mock_sale_instance

        with self.assertRaises(PayPalError):
            self.client.refund_payment(
                sale_id='SALE-TEST123',
                amount=Decimal('100.00')
            )

    @patch('paypalrestsdk.Sale')
    def test_refund_payment_full_amount(self, mock_sale):
        """Prueba el reembolso completo de un pago"""
        # Simula reembolso exitoso
        mock_refund = MagicMock()
        mock_refund.success.return_value = True
        mock_refund.id = 'REFUND-TEST123'
        mock_refund.state = 'completed'
        mock_refund.amount = {'total': '100.00', 'currency': 'USD'}
        
        mock_sale_instance = MagicMock()
        mock_sale_instance.amount = MagicMock(currency='USD')
        mock_sale_instance.refund.return_value = mock_refund
        mock_sale.find.return_value = mock_sale_instance

        result = self.client.refund_payment(sale_id='SALE-TEST123')
        
        self.assertEqual(result['id'], 'REFUND-TEST123')
        self.assertEqual(result['state'], 'completed')

    def test_paypal_error_inheritance(self):
        """Prueba que PayPalError hereda correctamente de APIException"""
        error = PayPalError('Test error')
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.default_detail, 'Error al procesar la operación con PayPal')
        self.assertEqual(error.default_code, 'paypal_error')