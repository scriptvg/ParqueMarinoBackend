# Parque Marino Backend - Documentación Completa del Sistema

## Tabla de Contenidos
1. [Descripción General del Sistema](#descripción-general-del-sistema)
2. [Arquitectura](#arquitectura)
3. [Tecnología Stack](#tecnología-stack)
4. [Documentación de Módulos](#documentación-de-módulos)
   - [Módulos de Negocio](#módulos-de-negocio)
   - [Módulos de Soporte](#módulos-de-soporte)
   - [Módulos de Integración](#módulos-de-integración)
5. [Documentación de la API](#documentación-de-la-api)
6. [Modelos de Datos](#modelos-de-datos)
7. [Seguridad](#seguridad)
8. [Despliegue](#despliegue)
9. [Pruebas](#pruebas)
10. [Solución de Problemas](#solución-de-problemas)

## Descripción General del Sistema

El Parque Marino Backend es un sistema integral basado en Django diseñado para soportar todas las operaciones digitales de un parque marino o acuario. Proporciona APIs RESTful para gestionar vida silvestre, programas educativos, exhibiciones, infraestructura, gestión de documentos, pagos, tickets y control de acceso de usuarios.

### Características Clave

- **Gestión de Vida Silvestre**: Seguimiento de especies, animales, hábitats y estado de conservación
- **Programas Educativos**: Gestión de programas, programación de instructores y seguimiento de inscripciones
- **Exhibiciones**: Gestión de contenido para exhibiciones con imágenes, descripciones y elementos interactivos
- **Gestión de Infraestructura**: Gestión de secciones físicas y hábitats
- **Gestión de Documentos**: Carga de archivos, versionado y seguimiento de acceso
- **Procesamiento de Pagos**: Manejo seguro de pagos a través de Stripe y PayPal con facturación electrónica
- **Sistema de Tickets**: Programación de visitas y gestión de tickets
- **Registro de Auditoría**: Seguimiento completo de todas las operaciones críticas
- **Autenticación de Usuarios**: Autenticación segura basada en JWT y control de acceso basado en roles
- **Sistema de Mensajería**: Funcionalidad de SMS y OTP a través de integración con Twilio

### Usuarios Objetivo

- **Administradores**: Acceso completo a todas las funciones del sistema
- **Personal**: Acceso a módulos específicos basados en roles
- **Visitantes**: Acceso limitado para compras de tickets e inscripciones a programas
- **Desarrolladores**: Acceso a la API para integración con sistemas externos

## Arquitectura

### Arquitectura de Alto Nivel

El sistema sigue una arquitectura backend modular de Django con un diseño de API RESTful utilizando Django REST Framework (DRF). Está estructurado en múltiples aplicaciones Django, cada una encapsulando un dominio específico.

```
ParqueMarinoBackend/
├── api/                     # Capa de versionado de la API
│   └── v1/                  # Versión 1 de la API
├── apps/                    # Aplicaciones Django
│   ├── business/            # Módulos de lógica de negocio principal
│   │   ├── wildlife/        # Gestión de vida silvestre
│   │   ├── education/       # Programas educativos
│   │   ├── exhibitions/     # Contenido de exhibiciones
│   │   ├── infrastructure/  # Infraestructura física
│   │   ├── payments/        # Procesamiento de pagos
│   │   ├── tickets/         # Sistema de tickets
│   │   └── documents/       # Gestión de documentos
│   ├── support/             # Servicios de soporte
│   │   ├── security/        # Autenticación y autorización
│   │   ├── audit/           # Registro de auditoría
│   │   └── messaging/       # Funcionalidad de SMS y OTP
│   └── integrations/        # Integraciones de terceros
│       └── payments/        # Integraciones de pasarelas de pago
├── config/                  # Archivos de configuración
├── core/                    # Utilidades y bibliotecas compartidas
├── docs/                    # Documentación
├── templates/               # Plantillas de correo electrónico
└── tests/                   # Archivos de prueba
```

### Patrones de Diseño

1. **Patrón MVC**: A través de la estructura del framework de Django
2. **Diseño API RESTful**: Por URLs de aplicaciones y serializadores
3. **Patrón Middleware**: Para registro de auditoría
4. **Patrón de Señales**: Señales de Django utilizadas en aplicaciones para lógica basada en eventos
5. **Patrón de Capa de Servicio**: En payments/services.py para abstracción de lógica de negocio
6. **Enrutamiento de URLs por Módulo**: Cada aplicación tiene su propia configuración de URL

### Interacción de Componentes

1. **Clientes** (web/móvil) interactúan a través de APIs REST definidas en archivos urls.py
2. **Vistas** llaman a serializadores y lógica de servicio, que interactúan con modelos
3. **Señales** desencadenan efectos secundarios (ej., registros de auditoría, historial de documentos)
4. **Integraciones de pago** (stripe_client.py, paypal.py) se comunican con APIs externas
5. **Utilidades S3** en utils/s3_utils.py manejan operaciones de archivos

## Tecnología Stack

### Tecnologías Principales

- **Framework**: Django 5.2.3
- **Framework API**: Django REST Framework 3.16.0
- **Base de Datos**: SQLite (desarrollo), PostgreSQL/MySQL (producción)
- **Autenticación**: JWT a través de djangorestframework_simplejwt 5.5.0
- **Caché**: Redis a través de django-redis 6.0.0
- **Almacenamiento**: AWS S3 a través de django-storages 1.14.6 y boto3 1.40.16

### Integraciones de Pago

- **Stripe**: 10.10.0
- **PayPal**: Integración personalizada

### Servicios de Comunicación

- **Twilio**: 8.8.0 para funcionalidad de SMS y OTP

### Herramientas de Desarrollo

- **Documentación**: drf-spectacular 0.28.0 y drf-yasg 1.21.10
- **Gestión de Entorno**: python-dotenv 0.19.2
- **Servidor Web**: Gunicorn 23.0.0 con whitenoise 6.9.0 para archivos estáticos

### Dependencias

Consulte [requirements.txt](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/requirements.txt) para una lista completa de dependencias.

## Documentación de Módulos

### Módulos de Negocio

#### Gestión de Vida Silvestre (`apps/business/wildlife/`)

Gestiona todos los aspectos de la vida silvestre incluyendo especies, animales, hábitats y estado de conservación.

**Modelos Clave**:
- `ConservationStatus`: Clasificaciones de estado de conservación IUCN
- `Specie`: Información sobre especies animales
- `Animal`: Animales individuales en el parque
- `Habitat`: Hábitats físicos donde residen los animales

**Características Clave**:
- Seguimiento de especies y animales
- Gestión de hábitats con monitoreo de capacidad
- Reportes de estado de conservación
- Gestión de imágenes para especies

#### Educación (`apps/business/education/`)

Maneja programas educativos, instructores, horarios e inscripciones de estudiantes.

**Modelos Clave**:
- `Programa`: Programas educativos ofrecidos
- `Instructor`: Instructores que enseñan programas
- `Horario`: Horarios de clases
- `Inscripcion`: Inscripciones de estudiantes

**Características Clave**:
- Creación y gestión de programas
- Programación de instructores
- Seguimiento de inscripciones a clases
- Integración de pagos para tarifas de programas

#### Exhibiciones (`apps/business/exhibitions/`)

Gestiona el contenido de exhibiciones incluyendo imágenes, descripciones y elementos interactivos.

**Modelos Clave**:
- `Exhibicion`: Gestión de contenido de exhibiciones
- `ExhibicionImage`: Imágenes asociadas con exhibiciones
- `ExhibicionFact`: Hechos interesantes sobre exhibiciones
- `ExhibicionButton`: Botones interactivos en exhibiciones

**Características Clave**:
- Gestión de contenido para exhibiciones
- Gestión de galerías de imágenes
- Contenido de aprendizaje basado en hechos
- Elementos interactivos de exhibiciones

#### Infraestructura (`apps/business/infrastructure/`)

Gestiona la infraestructura física incluyendo secciones y hábitats.

**Modelos Clave**:
- `Seccion`: Secciones físicas del parque
- `Habitat`: Hábitats dentro de secciones

**Características Clave**:
- Mapeo de secciones
- Seguimiento de ubicación de hábitats
- Gestión de capacidad

#### Pagos (`apps/business/payments/`)

Maneja todo el procesamiento de pagos incluyendo donaciones, tarifas de programas y venta de tickets.

**Modelos Clave**:
- `Pago`: Modelo base de pago
- `PagoInscripcion`: Pagos para inscripciones a programas educativos
- `Donacion`: Donaciones al parque

**Características Clave**:
- Soporte multi-moneda (CRC y USD)
- Integración con Stripe y PayPal
- Facturación electrónica
- Seguimiento de estado de pagos
- Conversión de moneda