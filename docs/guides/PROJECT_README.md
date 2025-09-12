# Parque Marino Backend - Enhanced Architecture

This project is a Django-based backend system designed to support a marine park or aquarium's digital operations. It has been enhanced with a more scalable and maintainable architecture while preserving all existing functionality.

## Project Overview

The system provides APIs and administrative functionality for:
- Managing educational programs, wildlife, and exhibitions
- Handling document management
- Processing payments and tickets
- User access control and audit logging

## Enhanced Architecture

We've improved the project structure to follow a more scalable and maintainable architecture:

### Directory Structure
```
my_enterprise_backend/
├── manage.py
├── requirements.txt
├── pyproject.toml           # Poetry configuration
├── .env                     # Environment variables
├── .gitignore
├── docker/                  # Docker files
│   ├── Dockerfile
│   └── docker-compose.yml
├── config/                  # Main project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Common configuration
│   │   ├── dev.py           # Development configuration
│   │   └── prod.py          # Production configuration
│   ├── urls.py
│   └── wsgi.py
├── apps/                    # Django apps
│   ├── business/
│   │   ├── documents/
│   │   │   ├── migrations/
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── tests/
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── __init__.py
│   │   └── education/
│   │       ├── migrations/
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       ├── views.py
│   │       └── tests/
│   │           ├── test_models.py
│   │           ├── test_views.py
│   │           └── __init__.py
├── api/                     # API versioning
│   ├── v1/
│   │   ├── routers.py
│   │   ├── urls.py
│   │   ├── base_views.py
│   │   └── __init__.py
│   └── urls.py
├── core/                    # Internal utilities and libraries
│   ├── utils/
│   ├── middleware/
│   ├── permissions/
│   └── __init__.py
├── static/                  # Static files
├── media/                   # User uploaded files
└── tests/                   # General tests
    ├── conftest.py
    └── __init__.py
```

### Key Improvements
1. **Modular Directory Structure** - Clear separation of concerns
2. **Environment-Specific Settings** - Development and production configurations
3. **API Versioning** - Support for API evolution
4. **Organized Documentation** - Better information discovery

## Getting Started

### Prerequisites
- Python 3.10+
- pip (or Poetry for dependency management)
- Virtual environment (recommended)

### Installation

#### Using Poetry (Recommended)
```bash
# Clone the project
git clone <repository-url>
cd ParqueMarinoBackend

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Set up environment variables (via .env or settings)
# Example .env file:
# DEBUG=True
# SECRET_KEY=your-secret-key
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Using pip
```bash
# Clone the project
git clone <repository-url>
cd ParqueMarinoBackend

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (via .env or settings)
# Example .env file:
# DEBUG=True
# SECRET_KEY=your-secret-key
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Configuration

The project supports environment-specific configurations:
- Development: `config.settings.development`
- Production: `config.settings.production`

Set the `DJANGO_SETTINGS_MODULE` environment variable accordingly.

## API Endpoints

The API is organized by modules and supports versioning:
- `/api/v1/wildlife/` - Wildlife management
- `/api/v1/education/` - Educational programs
- `/api/v1/exhibitions/` - Exhibition content
- `/api/v1/payments/` - Payment processing
- `/api/v1/tickets/` - Ticket management
- `/api/v1/documents/` - Document management
- `/api/v1/audit/` - Audit logs
- `/api/v1/auth/` - Authentication
- `/api/v1/messaging/` - SMS and OTP functionality (Twilio integration)

## Documentation

Documentation is organized in the `docs/` directory:
- [API Documentation](docs/api/API_DOCUMENTATION.md)
- [Development Guide](docs/development/GUIA_DESARROLLO.md)
- [Deployment Instructions](docs/deployment/S3_FILE_DELETION_README.md)
- [Twilio Integration Guide](docs/development/TWILIO_INTEGRATION.md)

## Additional Resources

- [Migration Guide](MIGRATION_GUIDE.md) - How to adapt to the new structure
- [Architecture Overview](ARCHITECTURE.md) - Detailed architecture description
- [Summary of Changes](SUMMARY_OF_CHANGES.md) - Summary of all improvements
- [Frontend Testing Guide](FRONTEND_TESTING_GUIDE.md) - How to test the Twilio integration with frontend applications

## Technology Stack

- **Backend**: Django 5.2.3
- **API Framework**: Django REST Framework 3.16.0
- **Authentication**: JWT via djangorestframework_simplejwt
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Storage**: AWS S3 via django-storages
- **Caching**: Redis via django-redis
- **Payments**: Stripe 10.10.0
- **SMS/OTP**: Twilio via twilio-python

## Backward Compatibility

All existing functionality is preserved. The enhancements are additive and designed to improve maintainability without breaking existing code.

## License

This project is proprietary to Parque Marino and should not be distributed without permission.

## Docker Support

The project includes Docker configuration for easy deployment and development:

```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up --build
```

This will start the application along with PostgreSQL and Redis services.
