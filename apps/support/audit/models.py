from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    """Modelo para registrar las acciones y cambios en el sistema.
    
    Este modelo almacena información detallada sobre las operaciones realizadas
    en el sistema, incluyendo quién las realizó, cuándo, y qué cambios se hicieron.
    
    Attributes:
        timestamp (DateTimeField): Fecha y hora de la acción.
        user (ForeignKey): Usuario que realizó la acción.
        action (CharField): Tipo de acción realizada (crear, actualizar, eliminar).
        model (CharField): Modelo/entidad afectada por la acción.
        record_id (PositiveIntegerField): ID del registro afectado.
        details (TextField): Detalles adicionales de la acción.
    """
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Acción'
    )
    model = models.CharField(
        max_length=255,
        verbose_name='Modelo'
    )
    record_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID del registro'
    )
    details = models.TextField(
        blank=True,
        null=True,
        verbose_name='Detalles'
    )

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']

    def __str__(self):
        """Representación en cadena del registro de auditoría."""
        return f'{self.timestamp} - {self.user} - {self.action} - {self.model} - {self.record_id}'

# Create your models here.
