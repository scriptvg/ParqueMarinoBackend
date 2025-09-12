from rest_framework import serializers
from .models import (
    Exhibicion,
    ExhibicionImage,
    ExhibicionFacts,
    ExhibicionDescription,
    ExhibicionButtons
)

class ExhibicionImageSerializer(serializers.ModelSerializer):
    """Serializador para las imágenes de exhibiciones.
    
    Este serializador maneja la conversión de instancias ExhibicionImage
    a JSON y viceversa, incluyendo la validación de imágenes.
    """
    
    class Meta:
        model = ExhibicionImage
        fields = ['id', 'exhibicion', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ExhibicionFactsSerializer(serializers.ModelSerializer):
    """Serializador para los datos interesantes de exhibiciones.
    
    Este serializador maneja la conversión de instancias ExhibicionFacts
    a JSON y viceversa, incluyendo la validación de contenido.
    """
    
    class Meta:
        model = ExhibicionFacts
        fields = ['id', 'exhibicion', 'fact']

class ExhibicionDescriptionSerializer(serializers.ModelSerializer):
    """Serializador para las descripciones de exhibiciones.
    
    Este serializador maneja la conversión de instancias ExhibicionDescription
    a JSON y viceversa, incluyendo la validación de contenido.
    """
    
    class Meta:
        model = ExhibicionDescription
        fields = ['id', 'exhibicion', 'description']

class ExhibicionButtonsSerializer(serializers.ModelSerializer):
    """Serializador para los botones de exhibiciones.
    
    Este serializador maneja la conversión de instancias ExhibicionButtons
    a JSON y viceversa, incluyendo la validación de enlaces.
    """
    
    class Meta:
        model = ExhibicionButtons
        fields = ['id', 'exhibicion', 'label', 'link']

    def validate_link(self, value):
        """Valida que el enlace sea una URL válida si se proporciona."""
        if value and not value.startswith(('http://', 'https://', '/')):
            raise serializers.ValidationError(
                'El enlace debe ser una URL válida que comience con http://, https:// o /'
            )
        return value

class ExhibicionSerializer(serializers.ModelSerializer):
    """Serializador principal para las exhibiciones.
    
    Este serializador maneja la conversión de instancias Exhibicion a JSON
    y viceversa, incluyendo relaciones anidadas con imágenes, datos,
    descripciones y botones.
    """
    
    images = ExhibicionImageSerializer(many=True, read_only=True)
    facts = ExhibicionFactsSerializer(many=True, read_only=True)
    descriptions = ExhibicionDescriptionSerializer(many=True, read_only=True)
    buttons = ExhibicionButtonsSerializer(many=True, read_only=True)

    class Meta:
        model = Exhibicion
        fields = ['id', 'value', 'label', 'title', 'images', 'facts', 'descriptions', 'buttons']

    def validate(self, data):
        """Valida que los campos únicos no se dupliquen."""
        # Verificar si estamos actualizando una instancia existente
        instance = getattr(self, 'instance', None)
        
        # Validar value
        if instance and instance.value != data.get('value'):
            if Exhibicion.objects.filter(value=data.get('value')).exists():
                raise serializers.ValidationError({
                    'value': 'Ya existe una exhibición con este valor.'
                })
        
        # Validar label
        if instance and instance.label != data.get('label'):
            if Exhibicion.objects.filter(label=data.get('label')).exists():
                raise serializers.ValidationError({
                    'label': 'Ya existe una exhibición con esta etiqueta.'
                })
        
        # Validar title
        if instance and instance.title != data.get('title'):
            if Exhibicion.objects.filter(title=data.get('title')).exists():
                raise serializers.ValidationError({
                    'title': 'Ya existe una exhibición con este título.'
                })
        
        return data
