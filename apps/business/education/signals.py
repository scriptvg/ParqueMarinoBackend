"""
Señales de Django para el módulo education

Este módulo define las señales que se ejecutan automáticamente cuando
ocurren eventos en los modelos del módulo education, específicamente
para gestionar la eliminación de archivos en S3.

Señales implementadas:
- post_delete: Elimina archivos de S3 cuando se elimina una instancia
- pre_save: Elimina archivos anteriores de S3 cuando se actualiza un campo de archivo
"""

import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import ServiciosEducativosImage, ProgramaEducativo
from core.utils.storage.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=ServiciosEducativosImage)
def delete_education_service_image_s3_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos S3 asociados cuando se elimina una imagen de servicio educativo
    
    Args:
        sender: Modelo que envía la señal (ServiciosEducativosImage)
        instance: Instancia que se está eliminando
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        results = delete_s3_files_from_instance(instance)
        logger.info(f"Eliminación S3 completada para imagen de servicio educativo ID {instance.pk}: {results}")
    except Exception as e:
        logger.error(f"Error al eliminar archivos S3 para imagen de servicio educativo ID {instance.pk}: {e}")

@receiver(pre_save, sender=ServiciosEducativosImage)
def delete_old_education_service_image_on_update(sender, instance, **kwargs):
    """
    Elimina la imagen anterior de S3 cuando se actualiza una imagen de servicio educativo
    
    Args:
        sender: Modelo que envía la señal (ServiciosEducativosImage)
        instance: Instancia que se está guardando (con cambios)
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        if instance.pk:  # Solo para actualizaciones, no para creaciones
            success = delete_old_s3_file(sender, instance, 'image')
            if not success:
                logger.warning(f"No se pudo eliminar la imagen anterior del servicio educativo ID {instance.pk}")
    except Exception as e:
        logger.error(f"Error al verificar imagen anterior para servicio educativo ID {instance.pk}: {e}")

@receiver(post_delete, sender=ProgramaEducativo)
def delete_educational_program_s3_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos S3 asociados cuando se elimina un programa educativo
    
    Args:
        sender: Modelo que envía la señal (ProgramaEducativo)
        instance: Instancia que se está eliminando
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        results = delete_s3_files_from_instance(instance)
        logger.info(f"Eliminación S3 completada para programa educativo '{instance.title}': {results}")
    except Exception as e:
        logger.error(f"Error al eliminar archivos S3 para programa educativo '{instance.title}': {e}")

@receiver(pre_save, sender=ProgramaEducativo)
def delete_old_educational_program_image_on_update(sender, instance, **kwargs):
    """
    Elimina la imagen anterior de S3 cuando se actualiza la imagen de un programa educativo
    
    Args:
        sender: Modelo que envía la señal (ProgramaEducativo)
        instance: Instancia que se está guardando (con cambios)
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        if instance.pk:  # Solo para actualizaciones, no para creaciones
            success = delete_old_s3_file(sender, instance, 'image')
            if not success:
                logger.warning(f"No se pudo eliminar la imagen anterior del programa educativo '{instance.title}'")
    except Exception as e:
        logger.error(f"Error al verificar imagen anterior para programa educativo '{instance.title}': {e}")