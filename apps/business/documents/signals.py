"""
Señales de Django para el módulo documents

Este módulo define las señales que se ejecutan automáticamente cuando
ocurren eventos en los modelos del módulo documents, específicamente
para gestionar la eliminación de archivos en S3.

Señales implementadas:
- post_delete: Elimina archivos de S3 cuando se elimina una instancia
- pre_save: Elimina archivos anteriores de S3 cuando se actualiza un campo de archivo
"""

import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Documento
from core.utils.storage.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Documento)
def delete_document_s3_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos S3 asociados cuando se elimina un documento
    
    Args:
        sender: Modelo que envía la señal (Documento)
        instance: Instancia que se está eliminando
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        results = delete_s3_files_from_instance(instance)
        logger.info(f"Eliminación S3 completada para documento '{instance.titulo}': {results}")
    except Exception as e:
        logger.error(f"Error al eliminar archivos S3 para documento '{instance.titulo}': {e}")

@receiver(pre_save, sender=Documento)
def delete_old_document_file_on_update(sender, instance, **kwargs):
    """
    Elimina el archivo anterior de S3 cuando se actualiza un documento
    
    Args:
        sender: Modelo que envía la señal (Documento)
        instance: Instancia que se está guardando (con cambios)
        **kwargs: Argumentos adicionales de la señal
    """
    try:
        if instance.pk:  # Solo para actualizaciones, no para creaciones
            success = delete_old_s3_file(sender, instance, 'archivo')
            if not success:
                logger.warning(f"No se pudo eliminar el archivo anterior del documento '{instance.titulo}'")
    except Exception as e:
        logger.error(f"Error al verificar archivo anterior para documento '{instance.titulo}': {e}")