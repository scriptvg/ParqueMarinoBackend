from django.db import models

class Ticket(models.Model):
    """Modelo para gestionar los tickets de entrada al parque marino.
    
    Este modelo almacena la información de los diferentes tipos de tickets
    disponibles para la venta, incluyendo su precio, nombre, descripción y
    control de cupos.
    
    Attributes:
        price (Decimal): Precio del ticket
        name (str): Nombre identificativo del ticket
        description (str): Descripción detallada del ticket
        total_slots (int): Número total de cupos disponibles
        occupied_slots (int): Número de cupos ocupados
        currency (str): Moneda del precio (CRC o USD)
    """
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio del Ticket"
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Nombre del Ticket"
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Descripción"
    )
    total_slots = models.PositiveIntegerField(
        default=1276,
        verbose_name="Cupos Totales"
    )
    occupied_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Cupos Ocupados"
    )
    currency = models.CharField(
        max_length=3,
        choices=[
            ('CRC', 'Colones'),
            ('USD', 'Dólares')
        ],
        default='CRC',
        verbose_name="Moneda"
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def has_available_slots(self, requested_slots):
        """Verifica si hay suficientes cupos disponibles.
        
        Args:
            requested_slots (int): Número de cupos solicitados
            
        Returns:
            bool: True si hay suficientes cupos, False en caso contrario
        """
        return self.total_slots - self.occupied_slots >= requested_slots

    def occupy_slots(self, slots):
        """Ocupa la cantidad especificada de cupos si están disponibles.
        
        Args:
            slots (int): Número de cupos a ocupar
            
        Returns:
            bool: True si se pudieron ocupar los cupos, False en caso contrario
        """
        if self.has_available_slots(slots):
            self.occupied_slots += slots
            self.save()
            return True
        return False

class Visit(models.Model):
    """Modelo para gestionar las visitas diarias al parque marino.
    
    Este modelo controla la disponibilidad de cupos para cada día de visita,
    permitiendo reservar y liberar cupos según sea necesario.
    
    Attributes:
        day (Date): Día de la visita
        total_slots (int): Número total de cupos disponibles por día
        occupied_slots (int): Número de cupos ocupados para ese día
    """
    day = models.DateField(
        verbose_name="Día de Visita",
        unique=True
    )
    total_slots = models.PositiveIntegerField(
        default=1276,
        verbose_name="Cupos Totales"
    )
    occupied_slots = models.PositiveIntegerField(
        default=0,
        verbose_name="Cupos Ocupados"
    )

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%Y-%m-%d')

    def has_available_slots(self, requested_slots):
        """Verifica si hay suficientes cupos disponibles para el día.
        
        Args:
            requested_slots (int): Número de cupos solicitados
            
        Returns:
            bool: True si hay suficientes cupos, False en caso contrario
        """
        return self.total_slots - self.occupied_slots >= requested_slots

    def occupy_slots(self, slots):
        """Ocupa la cantidad especificada de cupos si están disponibles.
        
        Args:
            slots (int): Número de cupos a ocupar
            
        Returns:
            bool: True si se pudieron ocupar los cupos, False en caso contrario
        """
        if self.has_available_slots(slots):
            self.occupied_slots += slots
            self.save()
            return True
        return False
