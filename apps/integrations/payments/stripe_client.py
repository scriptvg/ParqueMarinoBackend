"""Integración con Stripe para procesamiento de pagos con tarjeta"""

import logging
from decimal import Decimal
from typing import Dict, Optional

import stripe
from django.conf import settings
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class StripeClient:
    """Cliente para interactuar con la API de Stripe
    
    Esta clase maneja la configuración y las operaciones principales con Stripe,
    incluyendo pagos con tarjeta, tokens y reembolsos.
    
    Attributes:
        api_key (str): Clave secreta de API de Stripe
        public_key (str): Clave pública de API de Stripe
    """
    
    def __init__(self):
        """Inicializa el cliente de Stripe con la configuración desde settings"""
        self.api_key = settings.STRIPE_SECRET_KEY
        self.public_key = settings.STRIPE_PUBLIC_KEY
        stripe.api_key = self.api_key
    
    def create_payment_intent(self, amount: Decimal, currency: str, description: str) -> Dict:
        """Crea una intención de pago en Stripe
        
        Args:
            amount: Monto del pago (en centavos/céntimos)
            currency: Código de moneda (usd, crc)
            description: Descripción del pago
            
        Returns:
            Dict con la información de la intención de pago
            
        Raises:
            StripeError: Si hay un error al crear la intención de pago
        """
        try:
            # Stripe requiere montos en centavos/céntimos
            amount_cents = int(amount * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency.lower(),
                description=description,
                payment_method_types=['card']
            )
            
            logger.info(f'Intención de pago Stripe creada: {intent.id}')
            return {
                'id': intent.id,
                'client_secret': intent.client_secret,
                'amount': amount,
                'currency': currency,
                'status': intent.status
            }
            
        except stripe.error.StripeError as e:
            logger.error(f'Error Stripe al crear intención de pago: {str(e)}')
            raise StripeError(str(e))
        except Exception as e:
            logger.exception('Error inesperado al crear intención de pago Stripe')
            raise StripeError(str(e))
    
    def confirm_payment(self, payment_intent_id: str) -> Dict:
        """Confirma una intención de pago
        
        Args:
            payment_intent_id: ID de la intención de pago
            
        Returns:
            Dict con la información del pago confirmado
            
        Raises:
            StripeError: Si hay un error al confirmar el pago
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                logger.info(f'Pago Stripe confirmado: {intent.id}')
                return {
                    'id': intent.id,
                    'status': intent.status,
                    'amount': Decimal(intent.amount) / 100,  # Convertir de centavos
                    'currency': intent.currency,
                    'payment_method': intent.payment_method
                }
            else:
                logger.error(f'Estado inválido de pago Stripe: {intent.status}')
                raise StripeError(f'Estado de pago inválido: {intent.status}')
                
        except stripe.error.StripeError as e:
            logger.error(f'Error Stripe al confirmar pago: {str(e)}')
            raise StripeError(str(e))
        except Exception as e:
            logger.exception('Error inesperado al confirmar pago Stripe')
            raise StripeError(str(e))
    
    def refund_payment(self, payment_intent_id: str, amount: Optional[Decimal] = None) -> Dict:
        """Reembolsa un pago completado
        
        Args:
            payment_intent_id: ID de la intención de pago
            amount: Monto opcional a reembolsar. Si no se especifica, se reembolsa todo
            
        Returns:
            Dict con la información del reembolso
            
        Raises:
            StripeError: Si hay un error al procesar el reembolso
        """
        try:
            refund_data = {'payment_intent': payment_intent_id}
            
            if amount:
                refund_data['amount'] = int(amount * 100)  # Convertir a centavos
                
            refund = stripe.Refund.create(**refund_data)
            
            logger.info(f'Reembolso Stripe procesado: {refund.id}')
            return {
                'id': refund.id,
                'status': refund.status,
                'amount': Decimal(refund.amount) / 100,  # Convertir de centavos
                'currency': refund.currency
            }
            
        except stripe.error.StripeError as e:
            logger.error(f'Error Stripe al procesar reembolso: {str(e)}')
            raise StripeError(str(e))
        except Exception as e:
            logger.exception('Error inesperado al procesar reembolso Stripe')
            raise StripeError(str(e))

class StripeError(APIException):
    """Excepción personalizada para errores de Stripe
    
    Esta excepción se utiliza para manejar errores específicos de la integración
    con Stripe y proporcionar mensajes de error claros al cliente.
    """
    status_code = 400
    default_detail = 'Error al procesar la operación con Stripe'
    default_code = 'stripe_error'
