# Organización de la Documentación

Este documento explica cómo está organizada la documentación en el proyecto Parque Marino Backend.

## Estructura de Directorios

```
docs/
├── architecture/           # Documentos de arquitectura y diseño del sistema
├── business/               # Documentación de módulos de negocio
│   ├── documents/
│   ├── education/
│   ├── exhibitions/
│   ├── infrastructure/
│   ├── payments/
│   ├── tickets/
│   └── wildlife/
├── deployment/            # Guías de despliegue y configuración
├── guides/                # Guías y tutoriales generales
├── integrations/          # Documentación de integración de servicios de terceros
│   ├── paypal/
│   ├── stripe/
│   └── twilio/
├── support/               # Documentación de módulos de soporte
│   ├── audit/
│   ├── messaging/
│   └── security/
└── testing/               # Documentación y reportes de pruebas
```

## Descripciones de Directorios

### architecture/
Contiene documentos relacionados con la arquitectura general del sistema, incluyendo:
- Documentos de diseño del sistema
- Diagramas de arquitectura
- Resúmenes organizacionales
- Documentación de estructura del proyecto
- Resúmenes de reorganización
- Resúmenes de cambios

### business/
Contiene documentación específica para cada módulo de negocio:
- **documents/**: [Documentación del sistema de gestión de documentos](business/documents/DOCUMENTS_MODULE.md)
- **education/**: [Documentación de programas educativos](business/education/EDUCATION_MODULE.md)
- **exhibitions/**: [Documentación de gestión de exhibiciones](business/exhibitions/EXHIBITIONS_MODULE.md)
- **infrastructure/**: [Documentación de gestión de infraestructura](business/infrastructure/INFRASTRUCTURE_MODULE.md)
- **payments/**: [Documentación del sistema de pagos](business/payments/PAYMENTS_MODULE.md)
- **tickets/**: [Documentación del sistema de tickets](business/tickets/TICKETS_MODULE.md)
- **wildlife/**: [Documentación de gestión de vida silvestre](business/wildlife/WILDLIFE_MODULE.md)

### deployment/
Contiene documentación relacionada con el despliegue y configuración del sistema:
- Guías de migración
- Instrucciones de configuración
- Documentación de eliminación de archivos S3
- READMEs de despliegue

### guides/
Contiene guías y tutoriales generales para desarrolladores y usuarios:
- [Documentación de la API](guides/API_DOCUMENTATION.md)
- [Guía de Referencia Rápida](guides/QUICK_REFERENCE.md)
- Guías de desarrollo
- Guías de integración frontend
- README del proyecto
- Tutoriales generales

### integrations/
Contiene documentación para integraciones de servicios de terceros:
- **paypal/**: [Documentación de integración de PayPal](integrations/paypal/PAYPAL_INTEGRATION.md)
- **stripe/**: [Documentación de integración de Stripe](integrations/stripe/STRIPE_INTEGRATION.md)
- **twilio/**: [Documentación de integración de Twilio](integrations/twilio/TWILIO_INTEGRATION.md)

### support/
Contiene documentación para módulos de soporte:
- **audit/**: [Documentación de registro de auditoría](support/audit/AUDIT_MODULE.md)
- **messaging/**: [Documentación del sistema de mensajería](support/messaging/MESSAGING_MODULE.md)
- **security/**: [Documentación del sistema de seguridad](support/security/SECURITY_MODULE.md)

### testing/
Contiene documentación y reportes relacionados con pruebas:
- Reportes de pruebas
- Guías de pruebas
- Documentación de aseguramiento de calidad

## Convenciones de Nomenclatura de Archivos

- Utilice nombres descriptivos que indiquen claramente el contenido
- Utilice guiones bajos para separar palabras en nombres de archivos
- Utilice mayúsculas para la primera letra de cada palabra importante (Title Case)
- Termine los nombres de archivos con la extensión apropiada (.md para Markdown)

## Actualización de la Documentación

Al agregar nueva documentación:
1. Coloque los archivos en el directorio más apropiado basado en el contenido
2. Siga las convenciones de nomenclatura
3. Actualice este documento si agrega nuevas categorías
4. Asegúrese de que toda la documentación esté en formato Markdown para consistencia