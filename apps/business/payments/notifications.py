"""Sistema de notificaciones simple para pagos y facturación"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PaymentNotifier:
    """Manejador de notificaciones simples para pagos
    
    Esta clase se encarga de generar notificaciones simples que pueden
    ser usadas por el frontend como alertas.
    """
    
    def __init__(self):
        """Inicializa el notificador"""
        pass
    
    def send_payment_confirmation(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera notificación de pago exitoso para frontend
        
        Args:
            payment_data: Datos del pago realizado
            
        Returns:
            Dict con datos de notificación
        """
        notification = {
            'type': 'success',
            'title': 'Pago Confirmado',
            'message': f'El pago de {payment_data.get("monto", 0)} {payment_data.get("moneda", "CRC")} se ha procesado exitosamente.',
            'payment_id': payment_data.get('id'),
            'timestamp': payment_data.get('fecha_pago')
        }
        
        logger.info(f'Notificación de pago confirmado generada para pago {payment_data.get("id")}')
        return notification
    
    def send_payment_failed(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera notificación de pago fallido para frontend
        
        Args:
            payment_data: Datos del intento de pago
            
        Returns:
            Dict con datos de notificación
        """
        notification = {
            'type': 'error',
            'title': 'Pago Fallido',
            'message': f'El pago de {payment_data.get("monto", 0)} {payment_data.get("moneda", "CRC")} no se pudo procesar.',
            'payment_id': payment_data.get('id'),
            'timestamp': payment_data.get('fecha_pago')
        }
        
        logger.info(f'Notificación de pago fallido generada para pago {payment_data.get("id")}')
        return notification
    
    def send_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera notificación de factura para frontend
        
        Args:
            invoice_data: Datos de la factura
            
        Returns:
            Dict con datos de notificación
        """
        notification = {
            'type': 'info',
            'title': 'Factura Generada',
            'message': f'Factura generada por {invoice_data.get("monto", 0)} {invoice_data.get("moneda", "CRC")}.',
            'invoice_id': invoice_data.get('id'),
            'timestamp': invoice_data.get('fecha_creacion')
        }
        
        logger.info(f'Notificación de factura generada para factura {invoice_data.get("id")}')
        return notification
    
    def send_refund_confirmation(self, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera notificación de reembolso para frontend
        
        Args:
            refund_data: Datos del reembolso
            
        Returns:
            Dict con datos de notificación
        """
        notification = {
            'type': 'info',
            'title': 'Reembolso Procesado',
            'message': f'Reembolso de {refund_data.get("monto", 0)} {refund_data.get("moneda", "CRC")} procesado exitosamente.',
            'refund_id': refund_data.get('id'),
            'timestamp': refund_data.get('fecha_creacion')
        }
        
        logger.info(f'Notificación de reembolso generada para reembolso {refund_data.get("id")}')
        return notification

class EmailError(Exception):
    """Excepción personalizada para errores de email
    
    Esta excepción se utiliza para manejar errores específicos del envío
    de emails y proporcionar mensajes claros.
    """
    pass
