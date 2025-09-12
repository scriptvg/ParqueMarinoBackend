# Project Structure

This document outlines the organized structure of the Parque Marino Backend project.

## Directory Structure

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

## Key Directories

### `apps/`
Contains all Django applications organized by domain:
- `business/`: Core business logic applications
- `support/`: Support services (audit, security, messaging)
- `integrations/`: Third-party service integrations

### `config/`
Project configuration files:
- `settings/`: Environment-specific settings
- `urls.py`: Main URL routing
- `wsgi.py`: WSGI entry point

### `core/`
Internal utilities and shared libraries:
- `utils/`: Utility functions
- `middleware/`: Custom middleware
- `permissions/`: Custom permission classes

### `api/`
API versioning structure:
- `v1/`: Version 1 of the API
- Future versions can be added as needed

### `docker/`
Docker configuration files:
- `Dockerfile`: Application container definition
- `docker-compose.yml`: Multi-container setup

### `tests/`
General test files and configuration:
- `conftest.py`: Pytest configuration
- Test files for integration and end-to-end testing

## File Organization Principles

1. **Separation of Concerns**: Each directory has a specific purpose
2. **Modularity**: Apps are organized by business domain
3. **Scalability**: Structure supports future growth
4. **Maintainability**: Clear organization makes code easier to maintain
5. **Testability**: Tests are organized alongside the code they test

## Environment Configuration

- `.env`: Environment variables (not committed to version control)
- `config/settings/`: Environment-specific Django settings
- `pyproject.toml`: Poetry configuration for dependency management

## Deployment

- `docker/`: Containerization files for deployment
- `static/` and `media/`: File storage directories
- `requirements.txt`: Traditional pip dependencies (generated from Poetry)