from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from config.storage_backends import MediaStorage

User = get_user_model()

class ServiciosEducativos(models.Model):
    """Modelo para gestionar los servicios educativos
    
    Este modelo almacena la información principal de los servicios educativos
    ofrecidos por el zoológico.
    
    Attributes:
        value (CharField): Valor único identificador del servicio
        label (CharField): Etiqueta para mostrar del servicio
        title (CharField): Título del servicio
    """
    value = models.CharField(max_length=255, unique=True, null=False)
    label = models.CharField(max_length=255, unique=True, null=False)
    title = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        verbose_name = 'Servicio Educativo'
        verbose_name_plural = 'Servicios Educativos'

    def __str__(self):
        return self.value

class ServiciosEducativosImage(models.Model):
    """Modelo para las imágenes de servicios educativos
    
    Gestiona las imágenes asociadas a cada servicio educativo.
    
    Attributes:
        servicios_educativos (ForeignKey): Servicio educativo asociado
        image (ImageField): Imagen del servicio
        created_at (DateTimeField): Fecha de creación
        updated_at (DateTimeField): Fecha de última actualización
    """
    servicios_educativos = models.ForeignKey(ServiciosEducativos, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='servicios-educativos/', storage=MediaStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Imagen de Servicio Educativo'
        verbose_name_plural = 'Imágenes de Servicios Educativos'

class ServiciosEducativosFacts(models.Model):
    """Modelo para los datos relevantes de servicios educativos
    
    Almacena datos o hechos importantes sobre cada servicio educativo.
    
    Attributes:
        servicios_educativos (ForeignKey): Servicio educativo asociado
        fact (TextField): Dato o hecho relevante
    """
    servicios_educativos = models.ForeignKey(ServiciosEducativos, related_name='facts', on_delete=models.CASCADE)
    fact = models.TextField()

    class Meta:
        verbose_name = 'Dato de Servicio Educativo'
        verbose_name_plural = 'Datos de Servicios Educativos'

class ServiciosEducativosDescription(models.Model):
    """Modelo para las descripciones de servicios educativos
    
    Gestiona las descripciones detalladas de cada servicio educativo.
    
    Attributes:
        servicios_educativos (ForeignKey): Servicio educativo asociado
        description (TextField): Descripción del servicio
    """
    servicios_educativos = models.ForeignKey(ServiciosEducativos, related_name='descriptions', on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name = 'Descripción de Servicio Educativo'
        verbose_name_plural = 'Descripciones de Servicios Educativos'

class ServiciosEducativosButtons(models.Model):
    """Modelo para los botones de acción de servicios educativos
    
    Gestiona los botones y enlaces asociados a cada servicio educativo.
    
    Attributes:
        servicios_educativos (ForeignKey): Servicio educativo asociado
        label (CharField): Etiqueta del botón
        link (CharField): Enlace del botón
    """
    servicios_educativos = models.ForeignKey(ServiciosEducativos, related_name='buttons', on_delete=models.CASCADE)
    label = models.CharField(max_length=255, unique=True, null=False)
    link = models.CharField(max_length=255, unique=True, null=False, blank=True, default='')

    class Meta:
        verbose_name = 'Botón de Servicio Educativo'
        verbose_name_plural = 'Botones de Servicios Educativos'

class ProgramaEducativo(models.Model):
    """Modelo para los programas educativos
    
    Gestiona la información principal de los programas educativos ofrecidos.
    
    Attributes:
        title (CharField): Título del programa
        description (TextField): Descripción del programa
        image (ImageField): Imagen del programa
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='programas/', blank=True, null=True, storage=MediaStorage())

    class Meta:
        verbose_name = 'Programa Educativo'
        verbose_name_plural = 'Programas Educativos'

    def __str__(self):
        return self.title

class ProgramaItem(models.Model):
    """Modelo para los items de programas educativos
    
    Gestiona los elementos o características específicas de cada programa.
    
    Attributes:
        programa (ForeignKey): Programa educativo asociado
        text (CharField): Texto del item
    """
    programa = models.ForeignKey(ProgramaEducativo, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Item de Programa'
        verbose_name_plural = 'Items de Programas'

    def __str__(self):
        return f"{self.programa.title} - {self.text[:30]}"

class Instructor(models.Model):
    """Modelo para gestionar los instructores de programas educativos
    
    Este modelo almacena la información de los instructores que imparten
    los programas y servicios educativos en el zoológico.
    
    Attributes:
        user (ForeignKey): Relación con el modelo de usuario del sistema
        especialidad (CharField): Área de especialización del instructor
        experiencia_years (IntegerField): Años de experiencia en educación
        bio (TextField): Biografía o descripción del instructor
        activo (BooleanField): Estado activo/inactivo del instructor
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_profile')
    especialidad = models.CharField(max_length=100)
    experiencia_years = models.IntegerField(validators=[MinValueValidator(0)])
    bio = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructores'

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.especialidad}'

class Programa(models.Model):
    """Modelo para los programas educativos
    
    Gestiona la información de los programas educativos ofrecidos
    por el zoológico, incluyendo detalles como duración, capacidad y requisitos.
    
    Attributes:
        nombre (CharField): Nombre del programa educativo
        descripcion (TextField): Descripción detallada del programa
        duracion_horas (IntegerField): Duración total en horas
        capacidad_min (IntegerField): Número mínimo de participantes
        capacidad_max (IntegerField): Número máximo de participantes
        edad_minima (IntegerField): Edad mínima requerida
        edad_maxima (IntegerField): Edad máxima permitida
        requisitos (TextField): Requisitos para participar
        precio (DecimalField): Costo del programa
        activo (BooleanField): Estado activo/inactivo del programa
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion_horas = models.IntegerField(validators=[MinValueValidator(1)])
    capacidad_min = models.IntegerField(validators=[MinValueValidator(1)])
    capacidad_max = models.IntegerField(validators=[MinValueValidator(1)])
    edad_minima = models.IntegerField(validators=[MinValueValidator(0)])
    edad_maxima = models.IntegerField(validators=[MinValueValidator(0)])
    requisitos = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Programa Educativo'
        verbose_name_plural = 'Programas Educativos'

    def __str__(self):
        return self.nombre

class Horario(models.Model):
    """Modelo para gestionar los horarios de los programas
    
    Permite programar las sesiones de los programas educativos
    especificando fechas, horas y el instructor asignado.
    
    Attributes:
        programa (ForeignKey): Programa educativo asociado
        instructor (ForeignKey): Instructor asignado
        fecha_inicio (DateTimeField): Fecha y hora de inicio
        fecha_fin (DateTimeField): Fecha y hora de finalización
        cupos_disponibles (IntegerField): Lugares disponibles
        estado (CharField): Estado del horario (programado/en curso/finalizado/cancelado)
    """
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ]

    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='horarios')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='horarios_asignados')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    cupos_disponibles = models.IntegerField(validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f'{self.programa.nombre} - {self.fecha_inicio.strftime("%d/%m/%Y %H:%M")}'

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.cupos_disponibles = self.programa.capacidad_max
        super().save(*args, **kwargs)

# El modelo Pago ha sido movido a la aplicación payments como PagoInscripcion

class Inscripcion(models.Model):
    """Modelo para gestionar las inscripciones a programas
    
    Registra las inscripciones de los usuarios a los programas educativos,
    incluyendo información del participante y estado del pago.
    
    Attributes:
        horario (ForeignKey): Horario del programa seleccionado
        usuario (ForeignKey): Usuario que realiza la inscripción
        nombre_participante (CharField): Nombre del participante
        edad_participante (IntegerField): Edad del participante
        fecha_inscripcion (DateTimeField): Fecha y hora de la inscripción
        estado_pago (CharField): Estado del pago (pendiente/pagado/cancelado)
        notas (TextField): Notas adicionales sobre la inscripción
    """
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    ]

    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='inscripciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    nombre_participante = models.CharField(max_length=200)
    edad_participante = models.IntegerField(validators=[MinValueValidator(0)])
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return f'{self.nombre_participante} - {self.horario.programa.nombre}'

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva inscripción
            # Verificar edad del participante
            programa = self.horario.programa
            if not (programa.edad_minima <= self.edad_participante <= programa.edad_maxima):
                raise ValueError('La edad del participante no cumple con los requisitos del programa')
            
            # Verificar disponibilidad de cupos
            if self.horario.cupos_disponibles <= 0:
                raise ValueError('No hay cupos disponibles para este horario')
            
            # Reducir cupos disponibles
            self.horario.cupos_disponibles -= 1
            self.horario.save()
        
        super().save(*args, **kwargs)
