"""
Utilidades para gestión de archivos en S3

Este módulo proporciona funciones para gestionar archivos almacenados en S3,
incluyendo la eliminación automática cuando se eliminan registros de la base de datos.

Funciones principales:
- delete_s3_file: Elimina un archivo específico de S3
- delete_s3_files_from_instance: Elimina todos los archivos de una instancia de modelo
- get_file_fields_from_instance: Obtiene todos los campos de archivo de una instancia

Uso con signals:
```python
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .utils.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

@receiver(post_delete, sender=MiModelo)
def delete_s3_files_on_delete(sender, instance, **kwargs):
    delete_s3_files_from_instance(instance)

@receiver(pre_save, sender=MiModelo)
def delete_old_s3_file_on_update(sender, instance, **kwargs):
    if instance.pk:
        delete_old_s3_file(sender, instance, 'archivo')
```
"""

import logging
import boto3
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)

def get_s3_client():
    """
    Obtiene el cliente de S3 configurado
    
    Returns:
        boto3.client: Cliente de S3 configurado
        
    Raises:
        NoCredentialsError: Si no hay credenciales válidas
    """
    try:
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
        )
    except Exception as e:
        logger.error(f"Error al crear cliente S3: {e}")
        raise NoCredentialsError("No se pudieron obtener las credenciales de AWS")

def delete_s3_file(file_path):
    """
    Elimina un archivo específico de S3
    
    Args:
        file_path (str): Ruta del archivo en S3 (incluyendo prefijo media/)
        
    Returns:
        bool: True si se eliminó exitosamente, False en caso contrario
    """
    if not file_path:
        return False
        
    # Solo proceder si S3 está habilitado
    if not getattr(settings, 'USE_S3', False):
        logger.info(f"S3 no está habilitado, omitiendo eliminación de: {file_path}")
        return False
    
    try:
        # Usar el storage por defecto si está configurado para S3
        if hasattr(default_storage, 'delete'):
            default_storage.delete(file_path)
            logger.info(f"Archivo eliminado exitosamente de S3: {file_path}")
            return True
        else:
            # Fallback: usar boto3 directamente
            s3_client = get_s3_client()
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            
            # Asegurar que la ruta incluya el prefijo media/
            if not file_path.startswith('media/'):
                file_path = f"media/{file_path}"
            
            s3_client.delete_object(Bucket=bucket_name, Key=file_path)
            logger.info(f"Archivo eliminado exitosamente de S3: {file_path}")
            return True
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logger.warning(f"El archivo no existe en S3: {file_path}")
            return True  # Consideramos éxito si el archivo ya no existe
        else:
            logger.error(f"Error de cliente S3 al eliminar {file_path}: {e}")
            return False
    except NoCredentialsError:
        logger.error("Credenciales de AWS no disponibles")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al eliminar archivo de S3 {file_path}: {e}")
        return False

def get_file_fields_from_instance(instance):
    """
    Obtiene todos los campos de archivo (FileField/ImageField) de una instancia de modelo
    
    Args:
        instance: Instancia del modelo Django
        
    Returns:
        list: Lista de tuplas (nombre_campo, archivo) que contienen archivos
    """
    file_fields = []
    
    for field in instance._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            file_attr = getattr(instance, field.name)
            if file_attr and hasattr(file_attr, 'name') and file_attr.name:
                file_fields.append((field.name, file_attr))
    
    return file_fields

def delete_s3_files_from_instance(instance):
    """
    Elimina todos los archivos S3 asociados a una instancia de modelo
    
    Args:
        instance: Instancia del modelo Django
        
    Returns:
        dict: Resumen de archivos eliminados y errores
    """
    file_fields = get_file_fields_from_instance(instance)
    
    if not file_fields:
        logger.info(f"No hay archivos para eliminar en {instance.__class__.__name__} ID {instance.pk}")
        return {"deleted": 0, "errors": 0, "files": []}
    
    results = {"deleted": 0, "errors": 0, "files": []}
    
    for field_name, file_field in file_fields:
        try:
            file_path = file_field.name
            if delete_s3_file(file_path):
                results["deleted"] += 1
                results["files"].append({"field": field_name, "file": file_path, "status": "deleted"})
                logger.info(f"Eliminado archivo de campo '{field_name}': {file_path}")
            else:
                results["errors"] += 1
                results["files"].append({"field": field_name, "file": file_path, "status": "error"})
                logger.error(f"Error al eliminar archivo de campo '{field_name}': {file_path}")
        except Exception as e:
            results["errors"] += 1
            results["files"].append({"field": field_name, "file": str(file_field), "status": "exception", "error": str(e)})
            logger.error(f"Excepción al eliminar archivo de campo '{field_name}': {e}")
    
    logger.info(f"Resumen eliminación S3 para {instance.__class__.__name__} ID {instance.pk}: {results['deleted']} eliminados, {results['errors']} errores")
    return results

def delete_old_s3_file(model_class, instance, field_name):
    """
    Elimina el archivo anterior de S3 cuando un campo de archivo se actualiza
    
    Args:
        model_class: Clase del modelo
        instance: Nueva instancia (con cambios)
        field_name (str): Nombre del campo de archivo a verificar
        
    Returns:
        bool: True si se eliminó o no había archivo anterior, False en caso de error
    """
    if not instance.pk:
        return True  # Nueva instancia, no hay archivo anterior
    
    try:
        # Obtener la instancia anterior de la base de datos
        old_instance = model_class.objects.get(pk=instance.pk)
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)
        
        # Si el archivo cambió, eliminar el anterior
        if old_file and old_file.name and (not new_file or old_file.name != new_file.name):
            if delete_s3_file(old_file.name):
                logger.info(f"Eliminado archivo anterior de S3: {old_file.name}")
                return True
            else:
                logger.error(f"Error al eliminar archivo anterior de S3: {old_file.name}")
                return False
        
        return True  # No había cambio de archivo o no había archivo anterior
        
    except model_class.DoesNotExist:
        # La instancia no existe en la BD, probablemente es nueva
        return True
    except Exception as e:
        logger.error(f"Error al verificar archivo anterior para {field_name}: {e}")
        return False