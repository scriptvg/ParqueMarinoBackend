# Importaciones de Django
from django.db import models
from django.core.validators import MinValueValidator  # Para validar montos positivos
from config.storage_backends import MediaStorage

class Pago(models.Model):
    """Modelo base para gestionar pagos generales en el sistema
    
    Este modelo sirve como base para todos los tipos de pagos en el sistema.
    Incluye funcionalidades para:
    - Manejo de diferentes monedas (CRC y USD)
    - Conversión automática de montos
    - Seguimiento del estado del pago
    - Almacenamiento de comprobantes
    
    Para crear un nuevo pago:
    ```python
    pago = Pago.objects.create(
        monto=50000,
        moneda='CRC',
        metodo_pago='CARD',
        referencia_transaccion='REF123'
    )
    ```
    
    Para actualizar el estado de un pago:
    ```python
    pago.estado = 'SUCCESS'
    pago.save()
    ```
    
    Attributes:
        fecha_pago (DateTimeField): Fecha y hora automática del pago
        monto (DecimalField): Monto original del pago
        monto_crc (DecimalField): Monto convertido a Colones
        monto_usd (DecimalField): Monto convertido a Dólares
        moneda (CharField): Moneda original (CRC o USD)
        metodo_pago (CharField): Método de pago (CARD, PAYPAL, etc)
        referencia_transaccion (CharField): Identificador único del pago
        estado (CharField): Estado del pago (PENDING, SUCCESS, etc)
        comprobante (FileField): Documento de comprobante
        notas (TextField): Información adicional
    """
    METODO_PAGO_CHOICES = [
        ('CARD', 'Tarjeta de Crédito/Débito'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Efectivo/SINPE'),
        ('TRANSFER', 'Transferencia Bancaria'),
        ('OTHER', 'Otro')
    ]
    
    ESTADO_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'Procesando'),
        ('SUCCESS', 'Completado'),
        ('FAILED', 'Fallido'),
        ('REFUNDED', 'Reembolsado')
    ]

    MONEDA_CHOICES = [
        ('CRC', 'Colones'),
        ('USD', 'Dólares')
    ]

    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto en la moneda seleccionada'
    )
    monto_crc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto en Colones'
    )
    monto_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto en Dólares'
    )
    moneda = models.CharField(
        max_length=3,
        choices=MONEDA_CHOICES,
        default='CRC'
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES
    )
    referencia_transaccion = models.CharField(
        max_length=100,
        unique=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDING'
    )
    comprobante = models.FileField(
        upload_to='comprobantes_pago/',
        null=True,
        blank=True,
        storage=MediaStorage()
    )
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'Pago {self.referencia_transaccion} - {self.get_estado_display()}'
        
    def save(self, *args, **kwargs):
        """Guarda el pago y actualiza los montos en ambas monedas
        
        Antes de guardar, calcula y actualiza los montos en CRC y USD
        utilizando el servicio de conversión de divisas.
        """
        from .services import CurrencyConverter
        
        if not self.pk:  # Solo en creación
            monto_crc, monto_usd = CurrencyConverter.get_both_currencies(
                self.monto,
                self.moneda
            )
            self.monto_crc = monto_crc
            self.monto_usd = monto_usd
            
        super().save(*args, **kwargs)

class PagoInscripcion(Pago):
    """Modelo especializado para pagos de inscripciones educativas
    
    Este modelo hereda de Pago y añade funcionalidades específicas para
    manejar pagos de inscripciones a programas educativos.
    
    Características especiales:
    - Relación uno a uno con una inscripción
    - Actualización automática del estado de la inscripción
    - Validaciones específicas de montos según el programa
    
    Para crear un pago de inscripción:
    ```python
    pago = PagoInscripcion.objects.create(
        inscripcion=inscripcion,
        monto=inscripcion.programa.precio,
        moneda='CRC',
        metodo_pago='CARD',
        referencia_transaccion='INS123'
    )
    ```
    
    Estados de pago y su efecto en la inscripción:
    - SUCCESS -> estado_pago = 'pagado'
    - FAILED -> estado_pago = 'pendiente'
    - REFUNDED -> estado_pago = 'cancelado'
    
    Attributes:
        inscripcion (OneToOneField): Vínculo a la inscripción
    """
    inscripcion = models.OneToOneField(
        'education.Inscripcion',
        on_delete=models.CASCADE,
        related_name='pago'
    )

    class Meta:
        verbose_name = 'Pago de Inscripción'
        verbose_name_plural = 'Pagos de Inscripciones'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar estado de pago en la inscripción
        if self.estado == 'SUCCESS':
            self.inscripcion.estado_pago = 'pagado'
        elif self.estado == 'FAILED':
            self.inscripcion.estado_pago = 'pendiente'
        elif self.estado == 'REFUNDED':
            self.inscripcion.estado_pago = 'cancelado'
        self.inscripcion.save()

class Donacion(models.Model):
    """Modelo para gestionar donaciones al parque
    
    Este modelo maneja las donaciones voluntarias, permitiendo:
    - Donaciones anónimas o con información del donante
    - Diferentes monedas y métodos de pago
    - Seguimiento del estado de la donación
    - Conversión automática de montos
    
    Para crear una donación:
    ```python
    donacion = Donacion.objects.create(
        monto=100,
        moneda='USD',
        nombre_donante='Juan Pérez',
        email_donante='juan@ejemplo.com',
        metodo_pago='PAYPAL'
    )
    ```
    
    Para donaciones anónimas:
    ```python
    donacion = Donacion.objects.create(
        monto=50000,
        moneda='CRC',
        metodo_pago='CASH'
    )
    ```
    
    Attributes:
        monto (DecimalField): Cantidad de la donación
        moneda (CharField): Moneda original (CRC/USD)
        monto_crc (DecimalField): Monto en Colones
        monto_usd (DecimalField): Monto en Dólares
        nombre_donante (CharField): Nombre (opcional)
        email_donante (EmailField): Email (opcional)
        metodo_pago (CharField): Forma de pago
        referencia_transaccion (CharField): ID único
        estado (CharField): Estado del proceso
    """
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto original de la donación'
    )
    moneda = models.CharField(
        max_length=3,
        choices=Pago.MONEDA_CHOICES,
        default='CRC',
        help_text='Moneda original de la donación'
    )
    monto_crc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto convertido a Colones'
    )
    monto_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Monto convertido a Dólares'
    )
    nombre_donante = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    email_donante = models.EmailField(
        blank=True,
        null=True
    )
    metodo_pago = models.CharField(
        max_length=30,
        choices=Pago.METODO_PAGO_CHOICES
    )
    referencia_transaccion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    estado = models.CharField(
        max_length=20,
        choices=Pago.ESTADO_CHOICES,
        default='PENDING'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Donación {self.monto} {self.moneda} - {self.get_estado_display()}'
        
    def save(self, *args, **kwargs):
        """Guarda la donación y actualiza los montos en ambas monedas
        
        Antes de guardar, calcula y actualiza los montos en CRC y USD
        utilizando el servicio de conversión de divisas.
        """
        from .services import CurrencyConverter
        
        if not self.pk:  # Solo en creación
            monto_crc, monto_usd = CurrencyConverter.get_both_currencies(
                self.monto,
                self.moneda
            )
            self.monto_crc = monto_crc
            self.monto_usd = monto_usd
            
        super().save(*args, **kwargs)
