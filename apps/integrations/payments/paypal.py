"""Integración con PayPal para procesamiento de pagos"""

import logging
from decimal import Decimal
from typing import Dict, Optional

import paypalrestsdk
from django.conf import settings
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class PayPalClient:
    """Cliente para interactuar con la API de PayPal
    
    Esta clase maneja la configuración y las operaciones principales con PayPal,
    incluyendo la creación de pagos, ejecución y reembolsos.
    
    Attributes:
        is_sandbox (bool): Indica si se usa el entorno de sandbox o producción
        client_id (str): ID de cliente de PayPal
        client_secret (str): Secreto de cliente de PayPal
    """
    
    def __init__(self):
        """Inicializa el cliente de PayPal con la configuración desde settings"""
        self.is_sandbox = getattr(settings, 'PAYPAL_SANDBOX', True)
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        
        # Configurar SDK de PayPal
        paypalrestsdk.configure({
            'mode': 'sandbox' if self.is_sandbox else 'live',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
    
    def create_payment(self, amount: Decimal, currency: str, description: str) -> Dict:
        """Crea un nuevo pago en PayPal
        
        Args:
            amount: Monto del pago
            currency: Código de moneda (USD, CRC)
            description: Descripción del pago
            
        Returns:
            Dict con la información del pago creado, incluyendo URLs de redirección
            
        Raises:
            PayPalError: Si hay un error al crear el pago
        """
        try:
            payment = paypalrestsdk.Payment({
                'intent': 'sale',
                'payer': {
                    'payment_method': 'paypal'
                },
                'transactions': [{
                    'amount': {
                        'total': str(amount),
                        'currency': currency
                    },
                    'description': description
                }],
                'redirect_urls': {
                    'return_url': settings.PAYPAL_RETURN_URL,
                    'cancel_url': settings.PAYPAL_CANCEL_URL
                }
            })
            
            if payment.create():
                logger.info(f'Pago PayPal creado: {payment.id}')
                return {
                    'id': payment.id,
                    'links': payment.links,
                    'approval_url': next(
                        link.href for link in payment.links 
                        if link.rel == 'approval_url'
                    )
                }
            else:
                logger.error(f'Error al crear pago PayPal: {payment.error}')
                raise PayPalError('Error al crear el pago')
                
        except Exception as e:
            logger.exception('Error inesperado al crear pago PayPal')
            raise PayPalError(str(e))
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Dict:
        """Ejecuta un pago previamente creado y aprobado por el usuario
        
        Args:
            payment_id: ID del pago en PayPal
            payer_id: ID del pagador
            
        Returns:
            Dict con la información del pago ejecutado
            
        Raises:
            PayPalError: Si hay un error al ejecutar el pago
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({'payer_id': payer_id}):
                logger.info(f'Pago PayPal ejecutado: {payment_id}')
                return {
                    'id': payment.id,
                    'state': payment.state,
                    'transactions': payment.transactions
                }
            else:
                logger.error(f'Error al ejecutar pago PayPal: {payment.error}')
                raise PayPalError('Error al ejecutar el pago')
                
        except Exception as e:
            logger.exception('Error inesperado al ejecutar pago PayPal')
            raise PayPalError(str(e))
    
    def refund_payment(self, sale_id: str, amount: Optional[Decimal] = None) -> Dict:
        """Reembolsa un pago completado
        
        Args:
            sale_id: ID de la venta en PayPal
            amount: Monto opcional a reembolsar. Si no se especifica, se reembolsa todo
            
        Returns:
            Dict con la información del reembolso
            
        Raises:
            PayPalError: Si hay un error al procesar el reembolso
        """
        try:
            sale = paypalrestsdk.Sale.find(sale_id)
            refund_data = {}
            
            if amount:
                refund_data['amount'] = {
                    'total': str(amount),
                    'currency': sale.amount.currency
                }
                
            refund = sale.refund(refund_data)
            
            if refund.success():
                logger.info(f'Reembolso PayPal procesado: {refund.id}')
                return {
                    'id': refund.id,
                    'state': refund.state,
                    'amount': refund.amount
                }
            else:
                logger.error(f'Error al procesar reembolso PayPal: {refund.error}')
                raise PayPalError('Error al procesar el reembolso')
                
        except Exception as e:
            logger.exception('Error inesperado al procesar reembolso PayPal')
            raise PayPalError(str(e))

class PayPalError(APIException):
    """Excepción personalizada para errores de PayPal
    
    Esta excepción se utiliza para manejar errores específicos de la integración
    con PayPal y proporcionar mensajes de error claros al cliente.
    """
    status_code = 400
    default_detail = 'Error al procesar la operación con PayPal'
    default_code = 'paypal_error'
