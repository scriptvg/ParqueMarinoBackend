from rest_framework import serializers
from .models import Ticket, Visit

class TicketSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ticket.
    
    Este serializador maneja la conversión de instancias del modelo Ticket
    a JSON y viceversa, incluyendo validaciones y formateo de datos.
    
    Attributes:
        available_slots (int): Campo calculado que muestra los cupos disponibles
    """
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'name',
            'description',
            'price',
            'currency',
            'total_slots',
            'occupied_slots',
            'available_slots'
        ]
        read_only_fields = ['occupied_slots', 'available_slots']

    def get_available_slots(self, obj):
        """Calcula los cupos disponibles para el ticket.
        
        Args:
            obj: Instancia del modelo Ticket
            
        Returns:
            int: Número de cupos disponibles
        """
        return obj.total_slots - obj.occupied_slots

    def validate_price(self, value):
        """Valida que el precio sea mayor que cero.
        
        Args:
            value: Precio a validar
            
        Returns:
            Decimal: Precio validado
            
        Raises:
            serializers.ValidationError: Si el precio es menor o igual a cero
        """
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor que cero"
            )
        return value

class VisitSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Visit.
    
    Este serializador maneja la conversión de instancias del modelo Visit
    a JSON y viceversa, incluyendo validaciones y formateo de datos.
    
    Attributes:
        available_slots (int): Campo calculado que muestra los cupos disponibles
    """
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Visit
        fields = [
            'id',
            'day',
            'total_slots',
            'occupied_slots',
            'available_slots'
        ]
        read_only_fields = ['occupied_slots', 'available_slots']

    def get_available_slots(self, obj):
        """Calcula los cupos disponibles para el día de visita.
        
        Args:
            obj: Instancia del modelo Visit
            
        Returns:
            int: Número de cupos disponibles
        """
        return obj.total_slots - obj.occupied_slots

    def validate_day(self, value):
        """Valida que la fecha de visita no sea en el pasado.
        
        Args:
            value: Fecha a validar
            
        Returns:
            Date: Fecha validada
            
        Raises:
            serializers.ValidationError: Si la fecha es anterior a hoy
        """
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La fecha de visita no puede ser en el pasado"
            )
        return value
