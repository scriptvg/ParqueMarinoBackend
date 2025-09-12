from django.db import models
from config.storage_backends import MediaStorage

class Exhibicion(models.Model):
    """Modelo para gestionar las exhibiciones del zoológico.
    
    Este modelo almacena la información básica de cada exhibición, incluyendo
    su valor identificador, etiqueta y título.
    
    Attributes:
        value (str): Valor único identificador de la exhibición.
        label (str): Etiqueta descriptiva de la exhibición.
        title (str): Título principal de la exhibición.
    """
    
    value = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Valor',
        help_text='Identificador único de la exhibición'
    )
    label = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Etiqueta',
        help_text='Etiqueta descriptiva de la exhibición'
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Título',
        help_text='Título principal de la exhibición'
    )

    class Meta:
        verbose_name = 'Exhibición'
        verbose_name_plural = 'Exhibiciones'
        ordering = ['value']

    def __str__(self):
        return self.title

class ExhibicionImage(models.Model):
    """Modelo para gestionar las imágenes de las exhibiciones.
    
    Este modelo permite almacenar múltiples imágenes asociadas a una exhibición,
    incluyendo información sobre cuándo fueron creadas y actualizadas.
    
    Attributes:
        exhibicion (Exhibicion): Exhibición a la que pertenece la imagen.
        image (ImageField): Archivo de imagen.
        created_at (DateTime): Fecha y hora de creación.
        updated_at (DateTime): Fecha y hora de última actualización.
    """
    
    exhibicion = models.ForeignKey(
        Exhibicion,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Exhibición',
        help_text='Exhibición a la que pertenece la imagen'
    )
    image = models.ImageField(
        upload_to='exhibitions/',
        verbose_name='Imagen',
        help_text='Archivo de imagen de la exhibición',
        storage=MediaStorage()
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Imagen de exhibición'
        verbose_name_plural = 'Imágenes de exhibiciones'
        ordering = ['-created_at']

    def __str__(self):
        return f'Imagen de {self.exhibicion.title} ({self.created_at})'

class ExhibicionFacts(models.Model):
    """Modelo para gestionar datos interesantes de las exhibiciones.
    
    Este modelo permite almacenar múltiples datos o hechos interesantes
    asociados a una exhibición.
    
    Attributes:
        exhibicion (Exhibicion): Exhibición a la que pertenece el dato.
        fact (str): Dato o hecho interesante.
    """
    
    exhibicion = models.ForeignKey(
        Exhibicion,
        on_delete=models.CASCADE,
        related_name='facts',
        verbose_name='Exhibición',
        help_text='Exhibición a la que pertenece el dato'
    )
    fact = models.TextField(
        verbose_name='Dato interesante',
        help_text='Dato o hecho interesante sobre la exhibición'
    )

    class Meta:
        verbose_name = 'Dato de exhibición'
        verbose_name_plural = 'Datos de exhibiciones'

    def __str__(self):
        return f'Dato de {self.exhibicion.title}'

class ExhibicionDescription(models.Model):
    """Modelo para gestionar las descripciones de las exhibiciones.
    
    Este modelo permite almacenar múltiples descripciones detalladas
    asociadas a una exhibición.
    
    Attributes:
        exhibicion (Exhibicion): Exhibición a la que pertenece la descripción.
        description (str): Texto descriptivo.
    """
    
    exhibicion = models.ForeignKey(
        Exhibicion,
        on_delete=models.CASCADE,
        related_name='descriptions',
        verbose_name='Exhibición',
        help_text='Exhibición a la que pertenece la descripción'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Texto descriptivo de la exhibición'
    )

    class Meta:
        verbose_name = 'Descripción de exhibición'
        verbose_name_plural = 'Descripciones de exhibiciones'

    def __str__(self):
        return f'Descripción de {self.exhibicion.title}'

class ExhibicionButtons(models.Model):
    """Modelo para gestionar los botones de acción de las exhibiciones.
    
    Este modelo permite almacenar botones con enlaces asociados a una exhibición,
    útiles para proporcionar acciones o navegación adicional.
    
    Attributes:
        exhibicion (Exhibicion): Exhibición a la que pertenece el botón.
        label (str): Texto del botón.
        link (str): Enlace al que dirige el botón.
    """
    
    exhibicion = models.ForeignKey(
        Exhibicion,
        on_delete=models.CASCADE,
        related_name='buttons',
        verbose_name='Exhibición',
        help_text='Exhibición a la que pertenece el botón'
    )
    label = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Etiqueta',
        help_text='Texto que se mostrará en el botón'
    )
    link = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        default='',
        verbose_name='Enlace',
        help_text='URL a la que dirigirá el botón'
    )

    class Meta:
        verbose_name = 'Botón de exhibición'
        verbose_name_plural = 'Botones de exhibiciones'

    def __str__(self):
        return f'{self.label} - {self.exhibicion.title}'
