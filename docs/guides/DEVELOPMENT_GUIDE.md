# Guía de Desarrollo de la API

## Índice
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Guía de Modificación](#guía-de-modificación)
4. [Buenas Prácticas](#buenas-prácticas)
5. [Ejemplos Comunes](#ejemplos-comunes)
6. [Integración de Mensajería (Twilio)](#integración-de-mensajería-twilio)

## Estructura del Proyecto

El backend está organizado en las siguientes aplicaciones Django:

```
backend/
├── api/
│   ├── auth/            # Autenticación y usuarios
│   ├── documentos/      # Gestión de documentos
│   ├── exhibiciones/    # Exhibiciones del zoológico
│   ├── habitats/        # Hábitats de animales
│   ├── species/         # Especies de animales
│   └── visits/          # Gestión de visitas
├── education/           # Programas educativos
├── infrastructure/      # Infraestructura del zoológico
├── payments/            # Sistema de pagos
├── security/            # Seguridad y permisos
└── wildlife/            # Gestión de vida silvestre
```

## Configuración del Entorno

### Requisitos Previos

1. Python 3.8 o superior
2. PostgreSQL
3. Entorno virtual (recomendado)

### Instalación

1. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   - Crear archivo `.env` en la raíz del proyecto
   - Copiar variables desde `.env.example`

4. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

## Guía de Modificación

### Agregar Nuevo Modelo

1. Crear el modelo en `models.py`:
   ```python
   from django.db import models

   class NuevoModelo(models.Model):
       nombre = models.CharField(max_length=100)
       descripcion = models.TextField()
       fecha_creacion = models.DateTimeField(auto_now_add=True)

       class Meta:
           verbose_name = "Nuevo Modelo"
           verbose_name_plural = "Nuevos Modelos"

       def __str__(self):
           return self.nombre
   ```

2. Crear el serializador en `serializers.py`:
   ```python
   from rest_framework import serializers
   from .models import NuevoModelo

   class NuevoModeloSerializer(serializers.ModelSerializer):
       class Meta:
           model = NuevoModelo
           fields = '__all__'
   ```

3. Crear la vista en `views.py`:
   ```python
   from rest_framework import viewsets
   from .models import NuevoModelo
   from .serializers import NuevoModeloSerializer
   from api.permissions import IsAuthenticatedAndRole

   class NuevoModeloViewSet(viewsets.ModelViewSet):
       queryset = NuevoModelo.objects.all()
       serializer_class = NuevoModeloSerializer
       permission_classes = [IsAuthenticatedAndRole]
       http_method_names = ['get', 'post', 'put', 'delete']
   ```

4. Agregar URLs en `urls.py`:
   ```python
   from django.urls import path, include
   from rest_framework.routers import DefaultRouter
   from .views import NuevoModeloViewSet

   router = DefaultRouter()
   router.register('nuevo-modelo', NuevoModeloViewSet)

   urlpatterns = [
       path('', include(router.urls)),
   ]
   ```

5. Crear migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Modificar Modelo Existente

1. Actualizar el modelo en `models.py`:
   ```python
   class ModeloExistente(models.Model):
       # Campos existentes...
       nuevo_campo = models.CharField(max_length=100)  # Nuevo campo
   ```

2. Actualizar el serializador si es necesario:
   ```python
   class ModeloExistenteSerializer(serializers.ModelSerializer):
       class Meta:
           model = ModeloExistente
           fields = '__all__'  # O especificar campos incluyendo el nuevo
   ```

3. Crear y aplicar migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Buenas Prácticas

### Seguridad

1. Siempre usar `IsAuthenticatedAndRole` para proteger endpoints sensibles
2. No exponer información sensible en las respuestas API
3. Validar entrada de datos en serializers
4. Usar HTTPS en producción

### Rendimiento

1. Usar `select_related()` y `prefetch_related()` para optimizar consultas:
   ```python
   queryset = Modelo.objects.select_related('relacion').all()
   ```

2. Implementar paginación en listas largas:
   ```python
   from rest_framework.pagination import PageNumberPagination

   class CustomPagination(PageNumberPagination):
       page_size = 20
       page_size_query_param = 'page_size'
       max_page_size = 100
   ```

3. Usar caché cuando sea apropiado:
   ```python
   from django.core.cache import cache

   def get_queryset(self):
       cache_key = 'lista_modelos'
       queryset = cache.get(cache_key)
       if not queryset:
           queryset = super().get_queryset()
           cache.set(cache_key, queryset, timeout=300)
       return queryset
   ```

### Documentación

1. Documentar modelos con docstrings:
   ```python
   class Modelo(models.Model):
       """Descripción del modelo y su propósito.

       Attributes:
           campo1: Descripción del campo1
           campo2: Descripción del campo2
       """
       campo1 = models.CharField(max_length=100)
       campo2 = models.IntegerField()
   ```

2. Documentar vistas con docstrings:
   ```python
   class ModeloViewSet(viewsets.ModelViewSet):
       """ViewSet para gestionar modelos.

       Proporciona operaciones CRUD estándar.
       Requiere autenticación y rol específico.
       """
       queryset = Modelo.objects.all()
   ```

## Ejemplos Comunes

### Filtrar Resultados

``python
from django_filters import rest_framework as filters

class ModeloFilter(filters.FilterSet):
    nombre = filters.CharFilter(lookup_expr='icontains')
    fecha = filters.DateFilter()

    class Meta:
        model = Modelo
        fields = ['nombre', 'fecha']

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    filterset_class = ModeloFilter
```

### Personalizar Respuesta

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ModeloViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        modelo = self.get_object()
        stats = {
            'total': modelo.calcular_total(),
            'promedio': modelo.calcular_promedio()
        }
        return Response(stats)
```

### Manejo de Archivos

``python
from rest_framework.parsers import MultiPartParser, FormParser

class DocumentoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        archivo = self.request.FILES.get('archivo')
        serializer.save(archivo=archivo)
```

### Validaciones Personalizadas

```python
from rest_framework import serializers

class ModeloSerializer(serializers.ModelSerializer):
    def validate_campo(self, value):
        if alguna_condicion(value):
            raise serializers.ValidationError(
                "Mensaje de error personalizado"
            )
        return value

    def validate(self, data):
        if data['campo1'] > data['campo2']:
            raise serializers.ValidationError(
                "campo1 no puede ser mayor que campo2"
            )
        return data
```

## Notas Adicionales

1. Mantener actualizadas las dependencias del proyecto
2. Realizar pruebas antes de desplegar cambios
3. Seguir las convenciones de código de Django y DRF
4. Documentar cambios significativos en el código
5. Usar herramientas de análisis de código (pylint, flake8)

## Integración de Mensajería (Twilio)

El sistema ahora incluye integración con Twilio para enviar mensajes SMS y validar códigos OTP (One-Time Password). Esta funcionalidad se encuentra en la aplicación `messaging` dentro del directorio `apps/support`.

### Componentes Principales

1. **Modelo OTPRecord**: Almacena registros de códigos OTP enviados
2. **Servicio TwilioService**: Maneja la comunicación con la API de Twilio
3. **Vistas API**: Endpoints para enviar y verificar OTPs
4. **Serializadores**: Validan los datos de entrada para las operaciones OTP

### Uso Básico

Para usar la funcionalidad de mensajería:

1. Configurar las variables de entorno de Twilio en el archivo `.env`
2. Usar los endpoints de la API:
   - `POST /api/v1/messaging/send-otp/` - Enviar OTP
   - `POST /api/v1/messaging/verify-otp/` - Verificar OTP

### Consideraciones de Costo

Dado el presupuesto limitado de $14.2747 para pruebas, se recomienda:

1. Usar credenciales de prueba de Twilio durante el desarrollo
2. Implementar límites de tasa para prevenir uso excesivo
3. Configurar tiempos de expiración cortos para los OTP (por defecto 10 minutos)
4. Usar números de teléfono de prueba proporcionados por Twilio

### Pruebas

Para probar la funcionalidad de mensajería:

1. Ejecutar el script de prueba manual:
   ```bash
   python manual_messaging_test.py
   ```

2. Para pruebas de integración con Twilio:
   ```bash
   python test_twilio_integration.py
   ```

3. Para pruebas con frontend:
   - HTML/JavaScript Demo: Abre `frontend_twilio_demo.html` en tu navegador
   - React Demo: Navega a `frontend_react_demo` y ejecuta `npm install` seguido de `npm start`

Para más detalles, consultar la [Guía de Pruebas de Integración Twilio](TESTING_TWILIO_INTEGRATION.md), la [Guía de Integración de Twilio](TWILIO_INTEGRATION.md) y la [Guía de Pruebas de Frontend](../../FRONTEND_TESTING_GUIDE.md).