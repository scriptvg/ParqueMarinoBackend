"""
Señales de Django para el módulo payments

Este módulo define las señales que se ejecutan automáticamente cuando
ocurren eventos en los modelos del módulo payments, específicamente
para gestionar la eliminación de archivos en S3.

Señales implementadas:
- post_delete: Elimina archivos de S3 cuando se elimina una instancia
- pre_save: Elimina archivos anteriores de S3 cuando se actualiza un campo de archivo
"""

import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Pago
from core.utils.storage.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Pago)
def delete_payment_s3_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos S3 asociados cuando se elimina un pago
    
    Args:
        sender: Modelo que envía la señal (Pago)
        instance: Instancia que se está eliminando
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        results = delete_s3_files_from_instance(instance)
        logger.info(f"Eliminación S3 completada para pago ID {instance.pk}: {results}")
    except Exception as e:
        logger.error(f"Error al eliminar archivos S3 para pago ID {instance.pk}: {e}")

@receiver(pre_save, sender=Pago)
def delete_old_payment_receipt_on_update(sender, instance, **kwargs):
    """
    Elimina el comprobante anterior de S3 cuando se actualiza un pago
    
    Args:
        sender: Modelo que envía la señal (Pago)
        instance: Instancia que se está guardando (con cambios)
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        if instance.pk:  # Solo para actualizaciones, no para creaciones
            success = delete_old_s3_file(sender, instance, 'comprobante')
            if not success:
                logger.warning(f"No se pudo eliminar el comprobante anterior del pago ID {instance.pk}")
    except Exception as e:
        logger.error(f"Error al verificar comprobante anterior para pago ID {instance.pk}: {e}")