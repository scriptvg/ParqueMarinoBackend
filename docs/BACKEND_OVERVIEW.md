# Parque Marino Backend - Complete System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Module Documentation](#module-documentation)
   - [Business Modules](#business-modules)
   - [Support Modules](#support-modules)
   - [Integration Modules](#integration-modules)
5. [API Documentation](#api-documentation)
6. [Data Models](#data-models)
7. [Security](#security)
8. [Deployment](#deployment)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## System Overview

The Parque Marino Backend is a comprehensive Django-based system designed to support all digital operations of a marine park or aquarium. It provides RESTful APIs for managing wildlife, educational programs, exhibitions, infrastructure, document management, payments, tickets, and user access control.

### Key Features

- **Wildlife Management**: Species, animals, habitats, and conservation status tracking
- **Educational Programs**: Program management, instructor scheduling, and enrollment tracking
- **Exhibitions**: Content management for exhibits with images, descriptions, and interactive elements
- **Infrastructure Management**: Physical sections and habitat management
- **Document Management**: File upload, versioning, and access tracking
- **Payment Processing**: Secure payment handling via Stripe and PayPal with electronic invoicing
- **Ticketing System**: Visit scheduling and ticket management
- **Audit Logging**: Comprehensive tracking of all critical operations
- **User Authentication**: JWT-based secure authentication and role-based access control
- **Messaging System**: SMS and OTP functionality via Twilio integration

### Target Users

- **Administrators**: Full access to all system features
- **Staff**: Access to specific modules based on roles
- **Visitors**: Limited access for ticket purchases and program enrollments
- **Developers**: API access for integration with external systems

## Architecture

### High-Level Architecture

The system follows a modular Django backend architecture with a RESTful API design using Django REST Framework (DRF). It is structured into multiple Django apps, each encapsulating a specific domain.

```
ParqueMarinoBackend/
├── api/                     # API versioning layer
│   └── v1/                  # Version 1 of the API
├── apps/                    # Django applications
│   ├── business/            # Core business logic modules
│   │   ├── wildlife/        # Wildlife management
│   │   ├── education/       # Educational programs
│   │   ├── exhibitions/     # Exhibition content
│   │   ├── infrastructure/  # Physical infrastructure
│   │   ├── payments/        # Payment processing
│   │   ├── tickets/         # Ticketing system
│   │   └── documents/       # Document management
│   ├── support/             # Support services
│   │   ├── security/        # Authentication and authorization
│   │   ├── audit/           # Audit logging
│   │   └── messaging/       # SMS and OTP functionality
│   └── integrations/        # Third-party integrations
│       └── payments/        # Payment gateway integrations
├── config/                  # Configuration files
├── core/                    # Shared utilities and libraries
├── docs/                    # Documentation
├── templates/               # Email templates
└── tests/                   # Test files
```

### Design Patterns

1. **MVC Pattern**: Via Django's framework structure
2. **RESTful API Design**: Per app URLs and serializers
3. **Middleware Pattern**: For audit logging
4. **Signal Pattern**: Django signals used across apps for event-driven logic
5. **Service Layer Pattern**: In payments/services.py for business logic abstraction
6. **URL Routing by Module**: Each app has its own URL configuration

### Component Interaction

1. **Clients** (web/mobile) interact via REST APIs defined in urls.py files
2. **Views** call serializers and service logic, which interact with models
3. **Signals** trigger side effects (e.g., audit logs, document history)
4. **Payment integrations** (stripe_client.py, paypal.py) communicate with external APIs
5. **S3 utilities** in utils/s3_utils.py handle file operations

## Technology Stack

### Core Technologies

- **Framework**: Django 5.2.3
- **API Framework**: Django REST Framework 3.16.0
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Authentication**: JWT via djangorestframework_simplejwt 5.5.0
- **Caching**: Redis via django-redis 6.0.0
- **Storage**: AWS S3 via django-storages 1.14.6 and boto3 1.40.16

### Payment Integrations

- **Stripe**: 10.10.0
- **PayPal**: Custom integration

### Communication Services

- **Twilio**: 8.8.0 for SMS and OTP functionality

### Development Tools

- **Documentation**: drf-spectacular 0.28.0 and drf-yasg 1.21.10
- **Environment Management**: python-dotenv 0.19.2
- **Web Server**: Gunicorn 23.0.0 with whitenoise 6.9.0 for static files

### Dependencies

See [requirements.txt](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/requirements.txt) for a complete list of dependencies.

## Module Documentation

### Business Modules

#### Wildlife Management (`apps/business/wildlife/`)

Manages all aspects of wildlife including species, animals, habitats, and conservation status.

**Key Models**:
- `ConservationStatus`: IUCN conservation status classifications
- `Specie`: Information about animal species
- `Animal`: Individual animals in the park
- `Habitat`: Physical habitats where animals reside

**Key Features**:
- Species and animal tracking
- Habitat management with capacity monitoring
- Conservation status reporting
- Image management for species

#### Education (`apps/business/education/`)

Handles educational programs, instructors, schedules, and student enrollments.

**Key Models**:
- `Programa`: Educational programs offered
- `Instructor`: Instructors who teach programs
- `Horario`: Class schedules
- `Inscripcion`: Student enrollments

**Key Features**:
- Program creation and management
- Instructor scheduling
- Class enrollment tracking
- Payment integration for program fees

#### Exhibitions (`apps/business/exhibitions/`)

Manages exhibition content including images, descriptions, and interactive elements.

**Key Models**:
- `Exhibicion`: Exhibition content management
- `ExhibicionImage`: Images associated with exhibitions
- `ExhibicionFact`: Interesting facts about exhibits
- `ExhibicionButton`: Interactive buttons in exhibitions

**Key Features**:
- Content management for exhibits
- Image gallery management
- Fact-based learning content
- Interactive exhibit elements

#### Infrastructure (`apps/business/infrastructure/`)

Manages physical infrastructure including sections and habitats.

**Key Models**:
- `Seccion`: Physical sections of the park
- `Habitat`: Habitats within sections

**Key Features**:
- Section mapping
- Habitat location tracking
- Capacity management

#### Payments (`apps/business/payments/`)

Handles all payment processing including donations, program fees, and ticket sales.

**Key Models**:
- `Pago`: Base payment model
- `PagoInscripcion`: Payments for educational program enrollments
- `Donacion`: Donations to the park

**Key Features**:
- Multi-currency support (CRC and USD)
- Stripe and PayPal integration
- Electronic invoicing
- Payment status tracking
- Currency conversion

#### Tickets (`apps/business/tickets/`)

Manages ticket sales and visitor scheduling.

**Key Models**:
- `Ticket`: Individual tickets
- `Visita`: Scheduled visits

**Key Features**:
- Ticket creation and management
- Visit scheduling
- Capacity management
- Payment integration

#### Documents (`apps/business/documents/`)

Manages document uploads, versioning, and access tracking.

**Key Models**:
- `Documento`: Document management
- `TipoDocumento`: Document type classification
- `HistorialAcceso`: Document access history

**Key Features**:
- File upload and storage
- Document versioning
- Access tracking
- Type classification

### Support Modules

#### Security (`apps/support/security/`)

Handles authentication, authorization, and permissions.

**Key Features**:
- JWT-based authentication
- Role-based access control
- User management
- Password security

#### Audit (`apps/support/audit/`)

Provides comprehensive audit logging for all system operations.

**Key Models**:
- `AuditLog`: Detailed audit records

**Key Features**:
- Automatic logging of CRUD operations
- User action tracking
- Timestamped records
- Detailed change history

#### Messaging (`apps/support/messaging/`)

Handles SMS communication and OTP validation.

**Key Models**:
- `OTPRecord`: One-time password records

**Key Features**:
- Twilio integration for SMS
- OTP generation and validation
- Phone number verification
- Security-focused implementation

### Integration Modules

#### Payments (`apps/integrations/payments/`)

Contains specialized payment gateway integrations.

**Key Components**:
- `stripe_client.py`: Stripe API integration
- `paypal.py`: PayPal API integration

## API Documentation

The API is organized by modules and supports versioning with `/api/v1/` as the current stable version.

### Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### Core Endpoints

#### Authentication (`/api/v1/auth/`)
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /token/refresh/` - Refresh JWT token

#### Wildlife (`/api/v1/wildlife/`)
- `GET /species/` - List all species
- `POST /species/` - Create a new species
- `GET /species/{id}/` - Get species details
- `PUT /species/{id}/` - Update species
- `DELETE /species/{id}/` - Delete species
- Similar endpoints for animals, habitats, and conservation statuses

#### Education (`/api/v1/education/`)
- `GET /programas/` - List all programs
- `POST /programas/` - Create a new program
- `GET /instructores/` - List all instructors
- `POST /inscripciones/` - Create a new enrollment
- `GET /horarios/` - List all schedules

#### Payments (`/api/v1/payments/`)
- `POST /pagos/` - Create a new payment
- `POST /pagos/{id}/procesar_pago/` - Process payment with Stripe
- `POST /donaciones/` - Create a new donation
- `POST /donaciones/{id}/procesar_pago/` - Process donation with Stripe

#### Messaging (`/api/v1/messaging/`)
- `POST /send-otp/` - Send OTP to phone number
- `POST /verify-otp/` - Verify OTP code
- `GET /test-twilio/` - Test Twilio configuration

### Error Handling

The API follows standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

## Data Models

### Core Models Overview

#### User Management
- `User`: Django's built-in user model extended with custom permissions

#### Wildlife Models
- `ConservationStatus`: Conservation status classifications
- `Specie`: Animal species information
- `Animal`: Individual animals
- `Habitat`: Physical habitats

#### Education Models
- `Programa`: Educational programs
- `Instructor`: Program instructors
- `Horario`: Class schedules
- `Inscripcion`: Student enrollments

#### Payment Models
- `Pago`: Base payment model
- `PagoInscripcion`: Program enrollment payments
- `Donacion`: Donations

#### Document Models
- `Documento`: Document files
- `TipoDocumento`: Document types
- `HistorialAcceso`: Access history

### Relationships

The system uses Django's ORM relationships extensively:
- **ForeignKey**: One-to-many relationships
- **OneToOneField**: One-to-one relationships
- **ManyToManyField**: Many-to-many relationships

## Security

### Authentication

The system uses JWT (JSON Web Tokens) for authentication via `djangorestframework_simplejwt`.

### Authorization

Role-based access control is implemented through Django's permission system:
- **Administrators**: Full access
- **Staff**: Module-specific access
- **Users**: Limited access based on ownership

### Data Protection

- All sensitive data is stored encrypted
- Passwords are hashed using Django's built-in hashing
- Environment variables are used for secrets
- HTTPS is enforced in production

### API Security

- Rate limiting to prevent abuse
- CORS configuration for cross-origin requests
- Input validation on all endpoints
- SQL injection protection through ORM

## Deployment

### Environment Configuration

The system supports environment-specific configurations:
- Development: `config.settings.development`
- Production: `config.settings.production`

### Required Environment Variables

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### Production Deployment

1. Set up PostgreSQL or MySQL database
2. Configure AWS S3 for file storage
3. Set environment variables
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic`
6. Start server: `gunicorn config.wsgi:application`

### Docker Support

The project includes Docker configuration for easy deployment:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Testing

### Test Structure

Tests are organized by module in each app's `tests/` directory:
- `test_models.py`: Model validation tests
- `test_views.py`: API endpoint tests
- `test_services.py`: Business logic tests

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.business.wildlife

# Run with coverage
coverage run --source='.' manage.py test
```

### Test Coverage

The system includes comprehensive tests for:
- Model validation
- API endpoints
- Business logic
- Integration with external services
- Security features

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify database credentials in environment variables
   - Check database server status
   - Ensure required database drivers are installed

2. **S3 File Upload Issues**
   - Verify AWS credentials
   - Check bucket permissions
   - Ensure correct region configuration

3. **Payment Processing Failures**
   - Verify Stripe/PayPal API keys
   - Check webhook configurations
   - Review payment logs

4. **Authentication Problems**
   - Verify JWT configuration
   - Check user permissions
   - Review token expiration settings

### Logs

The system uses Django's logging framework with the following loggers:
- `django`: Django framework logs
- `apps`: Application-specific logs
- `payments`: Payment processing logs
- `audit`: Audit trail logs

### Monitoring

- Health check endpoints at `/api/v1/health/`
- Performance monitoring through database query logs
- Error tracking through exception logging