from rest_framework import serializers
from .models import Sections, Habitats

class SectionsSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Sections.
    
    Proporciona la serialización y deserialización de los datos de secciones,
    incluyendo validaciones y campos calculados.
    """
    num_habitats = serializers.IntegerField(read_only=True)
    habitats_list = serializers.SerializerMethodField()

    class Meta:
        model = Sections
        fields = ['id', 'name', 'num_habitats', 'habitats_list']

    def get_habitats_list(self, obj):
        """Obtiene la lista de hábitats asociados a la sección."""
        return [{
            'id': habitat.id,
            'name': habitat.name,
            'nums_animals': habitat.nums_animals
        } for habitat in obj.habitats.all()]

    def validate_name(self, value):
        """Valida que el nombre de la sección sea único y tenga un formato válido."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        
        # Verificar si el nombre ya existe (ignorando mayúsculas/minúsculas)
        if Sections.objects.filter(name__iexact=value.strip()).exists():
            if self.instance is None or self.instance.name.lower() != value.strip().lower():
                raise serializers.ValidationError("Ya existe una sección con este nombre")
                
        return value.strip()

class Habitats_Serializer(serializers.ModelSerializer):
    """Serializador para el modelo Habitats.
    
    Proporciona la serialización y deserialización de los datos de hábitats,
    incluyendo validaciones y campos calculados.
    """
    num_animals = serializers.IntegerField(read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Habitats
        fields = ['id', 'name', 'nums_animals', 'description', 'section', 'section_name', 'num_animals']
        
    def validate_name(self, value):
        """Valida que el nombre del hábitat sea único y tenga un formato válido."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value.strip()

    def validate_nums_animals(self, value):
        """Valida que el número de animales sea un valor positivo."""
        if value < 0:
            raise serializers.ValidationError("El número de animales no puede ser negativo")
        return value

    def validate_description(self, value):
        """Valida que la descripción tenga un formato válido."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres")
        return value.strip()
