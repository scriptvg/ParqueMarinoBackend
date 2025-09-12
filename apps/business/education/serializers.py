from rest_framework import serializers
from django.utils import timezone
from .models import (
    Instructor, Programa, Horario, Inscripcion,
    ServiciosEducativos, ServiciosEducativosImage, ServiciosEducativosFacts,
    ServiciosEducativosDescription, ServiciosEducativosButtons,
    ProgramaEducativo, ProgramaItem
)

class InstructorSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Instructor
    
    Gestiona la serialización y validación de datos para instructores,
    incluyendo validaciones específicas para años de experiencia.
    """
    class Meta:
        model = Instructor
        fields = ['id', 'user', 'especialidad', 'experiencia_years', 'bio', 'activo']

    def validate_experiencia_years(self, value):
        """Valida que los años de experiencia sean razonables"""
        if value > 50:
            raise serializers.ValidationError(
                'Los años de experiencia parecen ser demasiado altos'
            )
        return value

class ProgramaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Programa
    
    Maneja la serialización de programas educativos y valida
    las capacidades y edades especificadas.
    """
    class Meta:
        model = Programa
        fields = '__all__'

    def validate(self, data):
        """Valida las capacidades y edades del programa"""
        if data.get('capacidad_min') > data.get('capacidad_max'):
            raise serializers.ValidationError(
                'La capacidad mínima no puede ser mayor que la máxima'
            )
        
        if data.get('edad_minima') > data.get('edad_maxima'):
            raise serializers.ValidationError(
                'La edad mínima no puede ser mayor que la máxima'
            )

        return data

class HorarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Horario
    
    Gestiona los horarios de programas, validando la coherencia temporal
    y la disponibilidad del instructor.
    """
    class Meta:
        model = Horario
        fields = '__all__'

    def validate(self, data):
        """Valida la coherencia temporal y disponibilidad"""
        if data.get('fecha_inicio') >= data.get('fecha_fin'):
            raise serializers.ValidationError(
                'La fecha de inicio debe ser anterior a la fecha de fin'
            )

        if data.get('fecha_inicio') < timezone.now():
            raise serializers.ValidationError(
                'No se pueden crear horarios en el pasado'
            )

        # Verificar disponibilidad del instructor
        instructor = data.get('instructor')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        horarios_existentes = Horario.objects.filter(
            instructor=instructor,
            fecha_fin__gt=fecha_inicio,
            fecha_inicio__lt=fecha_fin
        ).exclude(estado='cancelado')

        if self.instance:
            horarios_existentes = horarios_existentes.exclude(pk=self.instance.pk)

        if horarios_existentes.exists():
            raise serializers.ValidationError(
                'El instructor ya tiene un horario asignado en este período'
            )

        return data

class InscripcionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Inscripcion
    
    Maneja las inscripciones a programas, validando la edad del participante
    y la disponibilidad de cupos.
    """
    class Meta:
        model = Inscripcion
        fields = '__all__'
        read_only_fields = ['fecha_inscripcion']

    def validate(self, data):
        """Valida la edad del participante y disponibilidad"""
        horario = data.get('horario')
        edad = data.get('edad_participante')
        
        # Validar edad del participante
        if not (horario.programa.edad_minima <= edad <= horario.programa.edad_maxima):
            raise serializers.ValidationError(
                'La edad del participante no cumple con los requisitos del programa'
            )

        # Validar disponibilidad de cupos
        if horario.cupos_disponibles <= 0:
            raise serializers.ValidationError(
                'No hay cupos disponibles para este horario'
            )

        # Validar estado del horario
        if horario.estado not in ['programado', 'en_curso']:
            raise serializers.ValidationError(
                'No se pueden realizar inscripciones en este horario'
            )

        return data

class ServiciosEducativosImageSerializer(serializers.ModelSerializer):
    """Serializador para las imágenes de servicios educativos
    
    Gestiona la serialización de imágenes asociadas a un servicio educativo.
    """
    class Meta:
        model = ServiciosEducativosImage
        fields = ['id', 'servicio', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ServiciosEducativosFactsSerializer(serializers.ModelSerializer):
    """Serializador para los datos relevantes de servicios educativos
    
    Maneja la serialización de hechos o datos importantes asociados a un servicio.
    """
    class Meta:
        model = ServiciosEducativosFacts
        fields = ['id', 'servicio', 'fact']

class ServiciosEducativosDescriptionSerializer(serializers.ModelSerializer):
    """Serializador para las descripciones de servicios educativos
    
    Gestiona la serialización de descripciones detalladas de un servicio.
    """
    class Meta:
        model = ServiciosEducativosDescription
        fields = ['id', 'servicio', 'description']

class ServiciosEducativosButtonsSerializer(serializers.ModelSerializer):
    """Serializador para los botones de acción de servicios educativos
    
    Maneja la serialización de botones interactivos asociados a un servicio.
    """
    class Meta:
        model = ServiciosEducativosButtons
        fields = ['id', 'servicio', 'label', 'link']

class ServiciosEducativosSerializer(serializers.ModelSerializer):
    """Serializador principal para servicios educativos
    
    Gestiona la serialización completa de un servicio educativo,
    incluyendo sus relaciones con imágenes, hechos, descripciones y botones.
    """
    images = ServiciosEducativosImageSerializer(many=True, read_only=True)
    facts = ServiciosEducativosFactsSerializer(many=True, read_only=True)
    descriptions = ServiciosEducativosDescriptionSerializer(many=True, read_only=True)
    buttons = ServiciosEducativosButtonsSerializer(many=True, read_only=True)

    class Meta:
        model = ServiciosEducativos
        fields = ['id', 'value', 'label', 'title', 'images', 'facts', 'descriptions', 'buttons']

    def create(self, validated_data):
        """Crea un nuevo servicio educativo con sus relaciones"""
        images_data = self.context.get('request').data.get('images', [])
        facts_data = self.context.get('request').data.get('facts', [])
        descriptions_data = self.context.get('request').data.get('descriptions', [])
        buttons_data = self.context.get('request').data.get('buttons', [])

        servicio = ServiciosEducativos.objects.create(**validated_data)

        for image_data in images_data:
            ServiciosEducativosImage.objects.create(servicio=servicio, **image_data)
        
        for fact_data in facts_data:
            ServiciosEducativosFacts.objects.create(servicio=servicio, **fact_data)
        
        for description_data in descriptions_data:
            ServiciosEducativosDescription.objects.create(servicio=servicio, **description_data)
        
        for button_data in buttons_data:
            ServiciosEducativosButtons.objects.create(servicio=servicio, **button_data)

        return servicio

    def update(self, instance, validated_data):
        """Actualiza un servicio educativo y sus relaciones"""
        instance.value = validated_data.get('value', instance.value)
        instance.label = validated_data.get('label', instance.label)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Actualizar relaciones si se proporcionan en el contexto
        if 'request' in self.context:
            if 'images' in self.context['request'].data:
                instance.images.all().delete()
                for image_data in self.context['request'].data['images']:
                    ServiciosEducativosImage.objects.create(servicio=instance, **image_data)
            
            if 'facts' in self.context['request'].data:
                instance.facts.all().delete()
                for fact_data in self.context['request'].data['facts']:
                    ServiciosEducativosFacts.objects.create(servicio=instance, **fact_data)
            
            if 'descriptions' in self.context['request'].data:
                instance.descriptions.all().delete()
                for description_data in self.context['request'].data['descriptions']:
                    ServiciosEducativosDescription.objects.create(servicio=instance, **description_data)
            
            if 'buttons' in self.context['request'].data:
                instance.buttons.all().delete()
                for button_data in self.context['request'].data['buttons']:
                    ServiciosEducativosButtons.objects.create(servicio=instance, **button_data)

        return instance

class ProgramaItemSerializer(serializers.ModelSerializer):
    """Serializador para los items de un programa educativo
    
    Gestiona la serialización de los elementos individuales que componen
    un programa educativo.
    """
    class Meta:
        model = ProgramaItem
        fields = ['id', 'programa', 'text']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    """Serializador para programas educativos
    
    Gestiona la serialización completa de un programa educativo,
    incluyendo sus items relacionados.
    """
    items = ProgramaItemSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramaEducativo
        fields = ['id', 'title', 'description', 'image', 'items']

    def create(self, validated_data):
        """Crea un nuevo programa educativo con sus items"""
        items_data = self.context.get('request').data.get('items', [])
        programa = ProgramaEducativo.objects.create(**validated_data)

        for item_data in items_data:
            ProgramaItem.objects.create(programa=programa, **item_data)

        return programa

    def update(self, instance, validated_data):
        """Actualiza un programa educativo y sus items"""
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        # Actualizar items si se proporcionan en el contexto
        if 'request' in self.context and 'items' in self.context['request'].data:
            instance.items.all().delete()
            for item_data in self.context['request'].data['items']:
                ProgramaItem.objects.create(programa=instance, **item_data)

        return instance
