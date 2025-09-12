# tests/test_stripe.py

from unittest.mock import patch, MagicMock
from django.test import TestCase
from decimal import Decimal
from apps.integrations.payments.stripe_client import StripeClient, StripeError

class TestStripeClient(TestCase):
    """Pruebas para la integración con Stripe
    
    Verifica la creación de intenciones de pago, confirmación de pagos
    y reembolsos a través de la API de Stripe.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = StripeClient(
            api_key='test_stripe_key',
            webhook_secret='test_webhook_secret'
        )
        
        self.payment_data = {
            'amount': Decimal('100.00'),
            'currency': 'usd',
            'payment_method_types': ['card'],
            'description': 'Curso de Programación',
            'metadata': {
                'order_id': 'ORDER123'
            }
        }

    @patch('stripe.PaymentIntent.create')
    def test_crear_payment_intent(self, mock_create):
        """Prueba la creación de una intención de pago"""
        # Simula respuesta exitosa de Stripe
        mock_create.return_value = MagicMock(
            id='pi_test123',
            client_secret='secret_test123',
            status='requires_payment_method'
        )

        intent = self.client.create_payment_intent(self.payment_data)
        
        self.assertEqual(intent['payment_intent_id'], 'pi_test123')
        self.assertEqual(intent['client_secret'], 'secret_test123')
        self.assertEqual(intent['status'], 'requires_payment_method')

    @patch('stripe.PaymentIntent.create')
    def test_error_crear_payment_intent(self, mock_create):
        """Prueba el manejo de errores al crear una intención de pago"""
        # Simula error de Stripe
        mock_create.side_effect = Exception('Invalid request')

        with self.assertRaises(StripeError):
            self.client.create_payment_intent(self.payment_data)

    @patch('stripe.PaymentIntent.confirm')
    def test_confirmar_payment_intent(self, mock_confirm):
        """Prueba la confirmación de una intención de pago"""
        # Simula confirmación exitosa
        mock_confirm.return_value = MagicMock(
            id='pi_test123',
            status='succeeded'
        )

        result = self.client.confirm_payment_intent(
            payment_intent_id='pi_test123',
            payment_method='pm_card_visa'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], 'succeeded')

    @patch('stripe.PaymentIntent.confirm')
    def test_error_confirmar_payment_intent(self, mock_confirm):
        """Prueba el manejo de errores al confirmar un pago"""
        # Simula error de tarjeta
        mock_confirm.side_effect = Exception('Card declined')

        with self.assertRaises(StripeError):
            self.client.confirm_payment_intent(
                payment_intent_id='pi_test123',
                payment_method='pm_card_visa'
            )

    @patch('stripe.Refund.create')
    def test_reembolso(self, mock_refund):
        """Prueba la creación de un reembolso"""
        # Simula reembolso exitoso
        mock_refund.return_value = MagicMock(
            id='re_test123',
            status='succeeded',
            amount=10000
        )

        result = self.client.create_refund(
            payment_intent_id='pi_test123',
            amount=Decimal('100.00')
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['refund_id'], 're_test123')

    def test_validacion_moneda(self):
        """Prueba la validación del código de moneda"""
        invalid_data = self.payment_data.copy()
        invalid_data['currency'] = 'INVALID'

        with self.assertRaises(ValueError):
            self.client.create_payment_intent(invalid_data)

    def test_conversion_monto(self):
        """Prueba la conversión de montos a centavos"""
        amount_cents = self.client._convert_amount_to_cents(Decimal('100.50'))
        self.assertEqual(amount_cents, 10050)

    @patch('stripe.WebhookSignature.verify_header')
    def test_verificar_webhook(self, mock_verify):
        """Prueba la verificación de firmas de webhook"""
        payload = b'{"type":"payment_intent.succeeded"}'
        signature = 'test_signature'

        # Simula verificación exitosa
        mock_verify.return_value = True

        event = self.client.verify_webhook(
            payload=payload,
            signature=signature
        )
        
        self.assertEqual(event['type'], 'payment_intent.succeeded')

    @patch('stripe.WebhookSignature.verify_header')
    def test_error_verificar_webhook(self, mock_verify):
        """Prueba el manejo de errores en la verificación de webhooks"""
        # Simula firma inválida
        mock_verify.side_effect = Exception('Invalid signature')

        with self.assertRaises(StripeError):
            self.client.verify_webhook(
                payload=b'{}',
                signature='invalid_signature'
            )

    @patch('stripe.PaymentIntent.retrieve')
    def test_obtener_payment_intent(self, mock_retrieve):
        """Prueba la obtención de detalles de una intención de pago"""
        # Simula respuesta con detalles
        mock_retrieve.return_value = MagicMock(
            id='pi_test123',
            status='succeeded',
            amount=10000,
            currency='usd'
        )

        intent = self.client.get_payment_intent('pi_test123')
        
        self.assertEqual(intent['payment_intent_id'], 'pi_test123')
        self.assertEqual(intent['status'], 'succeeded')

    @patch('stripe.PaymentMethod.attach')
    def test_adjuntar_payment_method(self, mock_attach):
        """Prueba adjuntar un método de pago a un cliente"""
        # Simula adjuntar método de pago exitosamente
        mock_attach.return_value = MagicMock(
            id='pm_test123',
            type='card'
        )

        result = self.client.attach_payment_method(
            payment_method_id='pm_test123',
            customer_id='cus_test123'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['payment_method_id'], 'pm_test123')
