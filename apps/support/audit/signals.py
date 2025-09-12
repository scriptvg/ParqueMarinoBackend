from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import reversion
from .models import AuditLog

@receiver(post_save)
def audit_log_create(sender, instance, created, **kwargs):
    """Signal para registrar creaciones y actualizaciones de modelos.
    
    Este signal se activa después de que un modelo es creado o actualizado,
    registrando la acción en el sistema de auditoría.
    
    Args:
        sender: El modelo que generó el signal.
        instance: La instancia del modelo que fue creada/actualizada.
        created: Boolean indicando si es una creación nueva.
        **kwargs: Argumentos adicionales del signal.
    """
    
    # Evitar recursión infinita al no registrar cambios en el propio modelo AuditLog
    if sender._meta.model_name != 'auditlog':
        action = 'created' if created else 'updated'
        
        with reversion.create_revision():
            # Establecer el usuario que realizó la acción
            reversion.set_user(
                getattr(instance, 'id_user', getattr(instance, 'user', None))
            )
            
            # Establecer un comentario descriptivo
            reversion.set_comment(
                f'Action {action} on {sender._meta.model_name} with id {instance.pk}'
            )
            
            # Crear el registro de auditoría
            AuditLog.objects.create(
                timestamp=timezone.now(),
                user=getattr(instance, 'id_user', getattr(instance, 'user', None)),
                action=action,
                model=sender._meta.model_name,
                record_id=instance.pk,
                details=f'Action {action} on {sender._meta.model_name} with id {instance.pk}'
            )

@receiver(post_delete)
def audit_log_delete(sender, instance, **kwargs):
    """Signal para registrar eliminaciones de modelos.
    
    Este signal se activa después de que un modelo es eliminado,
    registrando la acción en el sistema de auditoría.
    
    Args:
        sender: El modelo que generó el signal.
        instance: La instancia del modelo que fue eliminada.
        **kwargs: Argumentos adicionales del signal.
    """
    
    # Evitar recursión infinita al no registrar cambios en el propio modelo AuditLog
    if sender._meta.model_name != 'auditlog':
        with reversion.create_revision():
            # Establecer el usuario que realizó la acción
            reversion.set_user(
                getattr(instance, 'id_user', getattr(instance, 'user', None))
            )
            
            # Establecer un comentario descriptivo
            reversion.set_comment(
                f'Action deleted on {sender._meta.model_name} with id {instance.pk}'
            )
            
            # Crear el registro de auditoría
            AuditLog.objects.create(
                timestamp=timezone.now(),
                user=getattr(instance, 'id_user', getattr(instance, 'user', None)),
                action='deleted',
                model=sender._meta.model_name,
                record_id=instance.pk,
                details=f'Action deleted on {sender._meta.model_name} with id {instance.pk}'
            )