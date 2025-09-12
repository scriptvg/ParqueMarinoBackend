# Parque Marino Backend Architecture

This document describes the architecture of the Parque Marino Backend system and the improvements made to enhance scalability and maintainability.

## Overview

The Parque Marino Backend is a Django-based system that provides RESTful APIs for managing a marine park's digital operations. The system handles wildlife management, educational programs, exhibitions, payments, tickets, documents, and user access control.

## Architectural Improvements

### 1. Modular Directory Structure

The project now follows a more organized directory structure:

```
apps/
  business/     # Core business logic modules
  support/      # Support modules (security, audit)
  integrations/ # Third-party integrations
api/            # API layer with versioning
config/         # Configuration files
docs/           # Organized documentation
```

This structure provides:
- Clear separation of concerns
- Easier navigation and maintenance
- Better scalability for future growth
- Improved team collaboration

### 2. Environment-Specific Settings

Settings have been modularized:
- `base.py` - Common settings for all environments
- `development.py` - Development-specific configuration
- `production.py` - Production-specific configuration

Benefits:
- Reduced configuration errors
- Environment-specific optimizations
- Better security practices
- Easier deployment management

### 3. API Versioning

The API now supports versioning:
- `/api/v1/` - Current stable API version
- Standardized response formats
- Backward compatibility maintained

Benefits:
- Safer API evolution
- Better client support
- Easier deprecation management

### 4. Documentation Organization

Documentation is now organized by purpose:
- API documentation
- Development guides
- Deployment instructions

Benefits:
- Easier information discovery
- Better onboarding for new developers
- More maintainable documentation

## System Components

### Business Modules

1. **Wildlife** - Species, animals, habitats, conservation status
2. **Education** - Programs, instructors, schedules, enrollments
3. **Exhibitions** - Content management for exhibits
4. **Infrastructure** - Physical sections and habitats
5. **Payments** - Payment processing, donations, invoicing
6. **Tickets** - Ticketing and visit management
7. **Documents** - File management and versioning

### Support Modules

1. **Security** - Authentication, authorization, permissions
2. **Audit** - System logging and audit trails

### Integrations

1. **Payment Gateways** - Stripe and PayPal integrations

## Technology Stack

- **Framework**: Django 5.2.3
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT via djangorestframework_simplejwt
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Storage**: AWS S3 via django-storages
- **Caching**: Redis via django-redis
- **Payments**: Stripe 10.10.0
- **Documentation**: drf-spectacular, drf-yasg

## Data Flow

1. **Client Request** → API Layer → Business Logic → Database
2. **Business Logic** → Support Modules → Audit Logging
3. **External Services** → Payment Integrations → Business Logic
4. **File Storage** → S3 Integration → Business Logic

## Scalability Features

### Horizontal Scaling
- Stateless design allows for multiple server instances
- Redis caching reduces database load
- S3 storage offloads file management

### Vertical Scaling
- Modular design allows for focused optimization
- Database abstraction supports different backends
- Caching strategies can be tuned per module

### Future Enhancements
- Microservices potential for high-load modules
- Asynchronous task processing with Celery
- Advanced caching strategies
- Load balancing support

## Security Considerations

- JWT-based authentication
- CORS configuration
- Environment-specific security settings
- Audit logging for sensitive operations
- Secure payment processing

## Deployment Architecture

### Development
- SQLite database
- Local file storage
- Console email backend
- Debug mode enabled

### Production
- PostgreSQL/MySQL database
- AWS S3 file storage
- SMTP email backend
- Debug mode disabled
- Security headers enabled

## Monitoring and Maintenance

- Structured logging
- Audit trails
- Health check endpoints
- Performance monitoring hooks