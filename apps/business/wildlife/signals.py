"""
Señales de Django para el módulo wildlife

Este módulo define las señales que se ejecutan automáticamente cuando
ocurren eventos en los modelos del módulo wildlife, específicamente
para gestionar la eliminación de archivos en S3.

Señales implementadas:
- post_delete: Elimina archivos de S3 cuando se elimina una instancia
- pre_save: Elimina archivos anteriores de S3 cuando se actualiza un campo de archivo
"""

import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Specie
from core.utils.storage.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Specie)
def delete_specie_s3_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos S3 asociados cuando se elimina una especie
    
    Args:
        sender: Modelo que envía la señal (Specie)
        instance: Instancia que se está eliminando
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        results = delete_s3_files_from_instance(instance)
        logger.info(f"Eliminación S3 completada para especie '{instance.name}': {results}")
    except Exception as e:
        logger.error(f"Error al eliminar archivos S3 para especie '{instance.name}': {e}")

@receiver(pre_save, sender=Specie)
def delete_old_specie_image_on_update(sender, instance, **kwargs):
    """
    Elimina la imagen anterior de S3 cuando se actualiza la imagen de una especie
    
    Args:
        sender: Modelo que envía la señal (Specie)
        instance: Instancia que se está guardando (con cambios)
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        if instance.pk:  # Solo para actualizaciones, no para creaciones
            success = delete_old_s3_file(sender, instance, 'image')
            if not success:
                logger.warning(f"No se pudo eliminar la imagen anterior de la especie '{instance.name}'")
    except Exception as e:
        logger.error(f"Error al verificar imagen anterior para especie '{instance.name}': {e}")