from rest_framework import serializers

from .models import Specie, Animal, Habitat, ConservationStatus

class ConservationStatusSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de estados de conservación.
    
    Este serializador gestiona la conversión de los estados de conservación
    a formato JSON y viceversa, incluyendo validaciones básicas.
    """
    
    class Meta:
        model = ConservationStatus
        fields = ['id', 'name']

class SpecieSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de especies.
    
    Este serializador maneja la serialización de especies, incluyendo validaciones
    personalizadas y la gestión de relaciones.
    
    Attributes:
        conservation_status: Incluye los detalles del estado de conservación.
        animals_count: Número de animales de esta especie (solo lectura).
    """
    
    conservation_status = ConservationStatusSerializer(read_only=True)
    conservation_status_id = serializers.PrimaryKeyRelatedField(
        queryset=ConservationStatus.objects.all(),
        source='conservation_status',
        write_only=True
    )
    animals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Specie
        fields = [
            'id', 'name', 'scientific_name', 'description',
            'image', 'conservation_status', 'conservation_status_id',
            'animals_count'
        ]
        
    def get_animals_count(self, obj):
        """Calcula el número de animales de esta especie."""
        return obj.animals.count()
    
    def validate_scientific_name(self, value):
        """Valida que el nombre científico tenga el formato correcto."""
        if not ' ' in value:
            raise serializers.ValidationError(
                'El nombre científico debe incluir género y especie separados por espacio'
            )
        return value

class HabitatSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de hábitats.
    
    Este serializador gestiona la conversión de hábitats a JSON y viceversa,
    incluyendo información sobre su ocupación actual.
    
    Attributes:
        current_occupancy: Número actual de animales en el hábitat (solo lectura).
        is_full: Indica si el hábitat está a su capacidad máxima (solo lectura).
    """
    
    current_occupancy = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Habitat
        fields = [
            'id', 'name', 'capacity', 'description',
            'current_occupancy', 'is_full'
        ]
    
    def validate(self, data):
        """Valida que la capacidad sea un número positivo razonable."""
        if 'capacity' in data and data['capacity'] > 100:
            raise serializers.ValidationError(
                'La capacidad máxima no puede exceder 100 animales'
            )
        return data

class AnimalSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de animales.
    
    Este serializador maneja la conversión de animales a JSON y viceversa,
    incluyendo validaciones personalizadas y la gestión de relaciones.
    
    Attributes:
        specie: Incluye los detalles de la especie del animal.
        habitat: Incluye los detalles del hábitat del animal.
    """
    
    specie = SpecieSerializer(read_only=True)
    specie_id = serializers.PrimaryKeyRelatedField(
        queryset=Specie.objects.all(),
        source='specie',
        write_only=True
    )
    habitat = HabitatSerializer(read_only=True)
    habitat_id = serializers.PrimaryKeyRelatedField(
        queryset=Habitat.objects.all(),
        source='habitat',
        write_only=True
    )
    
    class Meta:
        model = Animal
        fields = [
            'id', 'name', 'age', 
            'specie', 'specie_id',
            'habitat', 'habitat_id'
        ]
    
    def validate_age(self, value):
        """Valida que la edad sea razonable."""
        if value > 100:
            raise serializers.ValidationError(
                'La edad parece ser demasiado alta'
            )
        return value
    
    def validate(self, data):
        """Valida que el hábitat no esté lleno al asignar un animal."""
        habitat = data.get('habitat')
        if habitat and habitat.is_full:
            raise serializers.ValidationError(
                'El hábitat seleccionado está a su capacidad máxima'
            )
        return data


