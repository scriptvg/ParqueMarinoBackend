from django.db import models
from config.storage_backends import MediaStorage

class ConservationStatus(models.Model):
    """Modelo para gestionar los estados de conservación de las especies.
    
    Este modelo almacena los diferentes estados de conservación según la clasificación
    internacional de la IUCN (Unión Internacional para la Conservación de la Naturaleza).
    
    Attributes:
        name (str): Nombre del estado de conservación, elegido de las opciones predefinidas.
    """
    
    STATUS_CHOICES = [
        ("LC", "Least Concern"),
        ("NT", "Near Threatened"),
        ("VU", "Vulnerable"),
        ("EN", "Endangered"),
        ("CR", "Critically Endangered"),
        ("EW", "Extinct in the Wild"),
        ("EX", "Extinct"),
    ]
    
    name = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        null=False,
        unique=True,
        verbose_name="Estado de Conservación",
        help_text="Estado de conservación según la clasificación IUCN"
    )

    class Meta:
        verbose_name = "Estado de Conservación"
        verbose_name_plural = "Estados de Conservación"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()

class Specie(models.Model):
    """Modelo para gestionar las especies de animales.
    
    Este modelo almacena la información básica de cada especie, incluyendo su
    nombre común, nombre científico y descripción.
    
    Attributes:
        name (str): Nombre común de la especie.
        scientific_name (str): Nombre científico de la especie (género y especie).
        description (str): Descripción detallada de la especie.
        image (ImageField): Imagen representativa de la especie.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre Común",
        help_text="Nombre común de la especie"
    )
    scientific_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre Científico",
        help_text="Nombre científico de la especie (género y especie)"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada de la especie"
    )
    image = models.ImageField(
        upload_to='species/',
        blank=True,
        null=True,
        verbose_name="Imagen",
        help_text="Imagen representativa de la especie",
        storage=MediaStorage()
    )
    conservation_status = models.ForeignKey(
        ConservationStatus,
        on_delete=models.PROTECT,
        related_name='species',
        verbose_name="Estado de Conservación",
        help_text="Estado actual de conservación de la especie"
    )

    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.scientific_name})"

    def get_image_url(self):
        """Obtiene la URL de la imagen de la especie si existe."""
        return self.image.url if self.image else None

class Animal(models.Model):
    """Modelo para gestionar los animales individuales del zoológico.
    
    Este modelo representa a cada animal individual, relacionándolo con su especie
    y registrando sus características particulares.
    
    Attributes:
        name (str): Nombre del animal.
        age (int): Edad del animal en años.
        specie (Specie): Especie a la que pertenece el animal.
        habitat (Habitat): Hábitat donde reside el animal.
    """
    
    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
        help_text="Nombre del animal"
    )
    age = models.PositiveIntegerField(
        verbose_name="Edad",
        help_text="Edad del animal en años"
    )
    specie = models.ForeignKey(
        Specie,
        on_delete=models.PROTECT,
        related_name='animals',
        verbose_name="Especie",
        help_text="Especie a la que pertenece el animal"
    )
    habitat = models.ForeignKey(
        'Habitat',
        on_delete=models.PROTECT,
        related_name='animals',
        verbose_name="Hábitat",
        help_text="Hábitat donde reside el animal"
    )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animales"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.specie.name}"

class Habitat(models.Model):
    """Modelo para gestionar los hábitats del zoológico.
    
    Este modelo representa los diferentes hábitats donde residen los animales,
    incluyendo su capacidad y características.
    
    Attributes:
        name (str): Nombre del hábitat.
        capacity (int): Capacidad máxima de animales.
        description (str): Descripción detallada del hábitat.
    """
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre",
        help_text="Nombre del hábitat"
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Capacidad",
        help_text="Capacidad máxima de animales"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del hábitat"
    )

    class Meta:
        verbose_name = "Hábitat"
        verbose_name_plural = "Hábitats"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def current_occupancy(self):
        """Calcula la ocupación actual del hábitat."""
        return self.animals.count()

    @property
    def is_full(self):
        """Verifica si el hábitat está a su capacidad máxima."""
        return self.current_occupancy >= self.capacity



    def get_image_url(self):
        if self.img:
          return self.img.url
        return None
    
