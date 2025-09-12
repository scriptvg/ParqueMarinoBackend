# Importaciones necesarias para los serializadores
from rest_framework import serializers
# Importamos los modelos que vamos a serializar
from .models import Pago, PagoInscripcion, Donacion

class PagoSerializer(serializers.ModelSerializer):
    """Serializador base para el modelo Pago
    
    Este serializador se encarga de convertir los objetos Pago a JSON y viceversa.
    También maneja la validación de datos antes de crear o actualizar un pago.
    
    Para usar este serializador:
    1. Crear un pago: 
       serializer = PagoSerializer(data=request.data)
       if serializer.is_valid():
           pago = serializer.save()
    
    2. Actualizar un pago:
       serializer = PagoSerializer(pago, data=request.data)
       if serializer.is_valid():
           pago = serializer.save()
    
    3. Obtener datos de un pago:
       serializer = PagoSerializer(pago)
       data = serializer.data
    
    Attributes:
        monto_crc (DecimalField): Monto en Colones (calculado automáticamente)
        monto_usd (DecimalField): Monto en Dólares (calculado automáticamente)
        client_secret (CharField): Secreto del cliente de Stripe (solo en respuestas de procesamiento)
    """
    monto_crc = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    monto_usd = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    client_secret = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = Pago
        fields = [
            'id',
            'fecha_pago',
            'monto',
            'monto_crc',
            'monto_usd',
            'moneda',
            'metodo_pago',
            'referencia_transaccion',
            'estado',
            'comprobante',
            'notas',
            'client_secret'
        ]
        read_only_fields = ['fecha_pago', 'monto_crc', 'monto_usd', 'client_secret']

    def validate_monto(self, value):
        """Valida que el monto sea mayor a cero"""
        if value <= 0:
            raise serializers.ValidationError(
                'El monto debe ser mayor a cero'
            )
        return value

    def validate_referencia_transaccion(self, value):
        """Valida que la referencia de transacción sea única"""
        if Pago.objects.filter(referencia_transaccion=value).exists():
            raise serializers.ValidationError(
                'Esta referencia de transacción ya existe'
            )
        return value
        
    def to_representation(self, instance):
        """Personaliza la representación del pago
        
        Añade información sobre los montos en ambas monedas y formatea
        los valores numéricos.
        """
        data = super().to_representation(instance)
        
        # Formatear montos con dos decimales
        for field in ['monto', 'monto_crc', 'monto_usd']:
            if data.get(field):
                data[field] = '{:.2f}'.format(float(data[field]))
                
        return data

class PagoInscripcionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo PagoInscripcion
    
    Este serializador maneja los pagos específicos de inscripciones a programas educativos.
    Hereda de ModelSerializer y realiza validaciones adicionales:
    - Verifica que la inscripción no tenga un pago previo
    - Valida que el monto coincida con el precio del programa
    
    Para usar este serializador:
    1. Crear un pago de inscripción:
       serializer = PagoInscripcionSerializer(data={
           'inscripcion': id_inscripcion,
           'monto': 50000,
           'moneda': 'CRC',
           'metodo_pago': 'TARJETA'
       })
    
    2. Validar y guardar:
       if serializer.is_valid():
           pago_inscripcion = serializer.save()
    """
    monto_crc = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    monto_usd = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    client_secret = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = PagoInscripcion
        fields = '__all__'
        read_only_fields = ['fecha_pago', 'monto_crc', 'monto_usd', 'client_secret']

    def validate(self, data):
        """Realiza validaciones adicionales para pagos de inscripción"""
        # Validar que la inscripción no tenga un pago existente
        inscripcion = data.get('inscripcion')
        if inscripcion and hasattr(inscripcion, 'pago'):
            raise serializers.ValidationError(
                'Esta inscripción ya tiene un pago asociado'
            )

        # Validar que el monto coincida con el precio del programa
        if inscripcion and data.get('monto') != inscripcion.horario.programa.precio:
            raise serializers.ValidationError(
                'El monto no coincide con el precio del programa'
            )

        return data

class DonacionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Donacion
    
    Este serializador gestiona las donaciones, incluyendo la validación de datos
    del donante y la conversión de monedas.
    
    Características principales:
    - Validación de montos positivos
    - Validación conjunta de email y nombre del donante
    - Conversión automática de montos entre CRC y USD
    
    Para usar este serializador:
    1. Crear una donación:
       serializer = DonacionSerializer(data={
           'monto': 100,
           'moneda': 'USD',
           'nombre_donante': 'Juan Pérez',
           'email_donante': 'juan@ejemplo.com',
           'metodo_pago': 'TRANSFERENCIA'
       })
    
    2. Validar y procesar:
       if serializer.is_valid():
           donacion = serializer.save()
    
    Attributes:
        monto_crc (DecimalField): Monto en Colones (calculado automáticamente)
        monto_usd (DecimalField): Monto en Dólares (calculado automáticamente)
        client_secret (CharField): Secreto del cliente de Stripe (solo en respuestas de procesamiento)
    """
    monto_crc = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    monto_usd = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    client_secret = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = Donacion
        fields = [
            'id',
            'monto',
            'monto_crc',
            'monto_usd',
            'moneda',
            'nombre_donante',
            'email_donante',
            'metodo_pago',
            'referencia_transaccion',
            'estado',
            'fecha_creacion',
            'client_secret'
        ]
        read_only_fields = ['fecha_creacion', 'monto_crc', 'monto_usd', 'client_secret']

    def validate_monto(self, value):
        """Valida que el monto de la donación sea mayor a cero"""
        if value <= 0:
            raise serializers.ValidationError(
                'El monto de la donación debe ser mayor a cero'
            )
        return value

    def validate(self, data):
        """Realiza validaciones adicionales para donaciones"""
        # Si se proporciona email, el nombre es requerido y viceversa
        email = data.get('email_donante')
        nombre = data.get('nombre_donante')
        if (email and not nombre) or (nombre and not email):
            raise serializers.ValidationError(
                'Debe proporcionar tanto el nombre como el email del donante'
            )
        return data
        
    def to_representation(self, instance):
        """Personaliza la representación de la donación
        
        Añade información sobre los montos en ambas monedas y formatea
        los valores numéricos.
        """
        data = super().to_representation(instance)
        
        # Formatear montos con dos decimales
        for field in ['monto', 'monto_crc', 'monto_usd']:
            if data.get(field):
                data[field] = '{:.2f}'.format(float(data[field]))
                
        return data